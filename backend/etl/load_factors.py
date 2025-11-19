"""
Main ETL script for loading factor data into the database.

Usage:
    python -m etl.load_factors --config ./backend/etl/config/global_factor_sources.yaml
"""
import os
import sys
import argparse
import yaml
import glob
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base, Country, FactorDefinition, FactorSeries, FactorReturn
from etl.parsers import get_parser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FactorETL:
    """ETL pipeline for factor data."""

    def __init__(self, config_path: str, data_dir: str):
        """
        Initialize ETL pipeline.

        Args:
            config_path: Path to YAML configuration file
            data_dir: Root directory for data files
        """
        self.config_path = config_path
        self.data_dir = Path(data_dir)
        self.config = self._load_config()
        self.db: Session = SessionLocal()

    def _load_config(self) -> Dict:
        """Load YAML configuration."""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from {self.config_path}")
        return config

    def initialize_factor_definitions(self):
        """Create or update factor definitions from config."""
        factor_defs = self.config.get('factor_definitions', [])

        for fd_config in factor_defs:
            # Check if factor definition exists
            fd = self.db.query(FactorDefinition).filter(
                FactorDefinition.code == fd_config['code']
            ).first()

            if fd:
                # Update existing
                fd.name = fd_config.get('name', fd.name)
                fd.group = fd_config.get('group', fd.group)
                fd.description = fd_config.get('description', fd.description)
                logger.info(f"Updated factor definition: {fd.code}")
            else:
                # Create new
                fd = FactorDefinition(
                    code=fd_config['code'],
                    name=fd_config['name'],
                    group=fd_config['group'],
                    description=fd_config.get('description')
                )
                self.db.add(fd)
                logger.info(f"Created factor definition: {fd.code}")

        self.db.commit()
        logger.info(f"Initialized {len(factor_defs)} factor definitions")

    def load_source(self, source_config: Dict):
        """
        Load data from a single source.

        Args:
            source_config: Source configuration dictionary
        """
        country_code = source_config['country_code']
        country_name = source_config['country_name']
        region_group = source_config.get('region_group', 'Other')
        source_name = source_config['source_name']
        frequency = source_config['frequency']
        currency = source_config.get('currency')
        file_pattern = source_config['file_pattern']
        parser_name = source_config['parser']

        logger.info(f"Processing source: {country_name} ({country_code}) - {source_name}")

        # Get or create country
        country = self.db.query(Country).filter(Country.code == country_code).first()
        if not country:
            country = Country(
                code=country_code,
                name=country_name,
                region_group=region_group
            )
            self.db.add(country)
            self.db.commit()
            logger.info(f"Created country: {country_name}")

        # Find data files
        pattern_path = self.data_dir / file_pattern
        data_files = glob.glob(str(pattern_path))

        if not data_files:
            logger.warning(f"No files found matching pattern: {pattern_path}")
            return

        logger.info(f"Found {len(data_files)} file(s) matching pattern")

        # Get parser
        parser_class = get_parser(parser_name)
        parser = parser_class()

        # Process each file
        for file_path in data_files:
            logger.info(f"Parsing file: {file_path}")
            try:
                # Parse file
                df = parser.parse(file_path, source_config)
                parser.validate_output(df)

                logger.info(f"Parsed {len(df)} return observations")

                # Group by factor code
                for factor_code in df['factor_code'].unique():
                    factor_df = df[df['factor_code'] == factor_code].copy()
                    self._load_factor_series(
                        country, factor_code, factor_df,
                        source_name, frequency, currency
                    )

            except Exception as e:
                logger.error(f"Error parsing {file_path}: {e}", exc_info=True)
                continue

    def _load_factor_series(
        self,
        country: Country,
        factor_code: str,
        df,
        source_name: str,
        frequency: str,
        currency: str
    ):
        """
        Load a single factor series into the database.

        Args:
            country: Country object
            factor_code: Canonical factor code
            df: DataFrame with date and return_value columns
            source_name: Name of data source
            frequency: Data frequency (Daily/Monthly)
            currency: Currency code
        """
        # Get factor definition
        factor_def = self.db.query(FactorDefinition).filter(
            FactorDefinition.code == factor_code
        ).first()

        if not factor_def:
            logger.warning(f"Factor definition not found for code: {factor_code}, skipping")
            return

        # Get or create factor series
        factor_series = self.db.query(FactorSeries).filter(
            FactorSeries.country_id == country.id,
            FactorSeries.factor_definition_id == factor_def.id,
            FactorSeries.frequency == frequency,
            FactorSeries.source_name == source_name
        ).first()

        if not factor_series:
            factor_series = FactorSeries(
                country_id=country.id,
                factor_definition_id=factor_def.id,
                source_name=source_name,
                frequency=frequency,
                currency=currency,
                start_date=df['date'].min().date(),
                end_date=df['date'].max().date()
            )
            self.db.add(factor_series)
            self.db.commit()
            logger.info(f"Created factor series: {country.code}/{factor_code}/{frequency}")
        else:
            # Update date range
            factor_series.start_date = min(factor_series.start_date, df['date'].min().date())
            factor_series.end_date = max(factor_series.end_date, df['date'].max().date())
            self.db.commit()

        # Load returns (upsert)
        returns_loaded = 0
        for _, row in df.iterrows():
            date = row['date'].date()
            return_value = float(row['return_value'])

            # Check if return exists
            existing = self.db.query(FactorReturn).filter(
                FactorReturn.factor_series_id == factor_series.id,
                FactorReturn.date == date
            ).first()

            if existing:
                # Update
                if existing.return_value != return_value:
                    existing.return_value = return_value
                    existing.updated_at = datetime.utcnow()
            else:
                # Insert
                factor_return = FactorReturn(
                    factor_series_id=factor_series.id,
                    date=date,
                    return_value=return_value
                )
                self.db.add(factor_return)
            returns_loaded += 1

            # Commit in batches
            if returns_loaded % 1000 == 0:
                self.db.commit()

        # Final commit
        self.db.commit()
        logger.info(f"Loaded {returns_loaded} returns for {country.code}/{factor_code}")

    def run(self):
        """Run the full ETL pipeline."""
        logger.info("Starting ETL pipeline")

        # Initialize factor definitions
        self.initialize_factor_definitions()

        # Load each source
        sources = self.config.get('sources', [])
        for source_config in sources:
            try:
                self.load_source(source_config)
            except Exception as e:
                logger.error(f"Error loading source {source_config.get('country_code')}: {e}",
                           exc_info=True)
                continue

        logger.info("ETL pipeline completed")
        self.db.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Load factor data into database')
    parser.add_argument(
        '--config',
        required=True,
        help='Path to YAML configuration file'
    )
    parser.add_argument(
        '--data-dir',
        default=os.getenv('DATA_DIR', './data'),
        help='Root directory for data files'
    )

    args = parser.parse_args()

    # Create database tables if they don't exist
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    # Run ETL
    etl = FactorETL(args.config, args.data_dir)
    etl.run()


if __name__ == '__main__':
    main()
