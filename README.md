# Global Factor Lab

A production-quality web application for exploring Fama-French-style equity factor datasets across multiple countries and regions. Think of it as a "country-by-country factor lab" that consolidates locally published factor data into one consistent, user-friendly interface.

## Features

- **Global Coverage**: Equity factor data from multiple countries (US, Sweden, UK, and more)
- **Rich Analytics**: Performance statistics, correlations, drawdowns, and rolling metrics
- **Clean UX**: Modern, responsive interface with interactive charts
- **Cross-Country Comparisons**: Compare factor performance across different markets
- **Extensible**: Easy to add new countries and factor datasets via configuration

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic migrations
- **Data Processing**: Pandas, NumPy

### Frontend
- **Framework**: Next.js (React) with TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **API Client**: Axios

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── db.py                   # Database connection and session management
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas for API
│   ├── requirements.txt        # Python dependencies
│   ├── alembic/                # Database migrations
│   │   ├── env.py
│   │   └── versions/
│   ├── api/                    # API endpoints
│   │   ├── countries.py        # Country-related endpoints
│   │   ├── factors.py          # Factor time series and stats
│   │   ├── analytics.py        # Cross-country analytics
│   │   └── analytics_utils.py  # Statistical calculations
│   └── etl/                    # ETL pipeline
│       ├── load_factors.py     # Main ETL script
│       ├── config/
│       │   └── global_factor_sources.yaml
│       └── parsers/            # Data parsers
│           ├── base_parser.py
│           ├── ken_french.py
│           └── generic_csv.py
├── frontend/
│   ├── pages/                  # Next.js pages
│   │   ├── index.tsx           # Home page
│   │   ├── about.tsx           # About page
│   │   ├── countries/          # Country listing
│   │   ├── country/[code].tsx  # Country detail
│   │   ├── factors/            # Factor listing
│   │   └── factor/[factorCode]/cross-country.tsx
│   ├── components/             # React components
│   │   ├── Layout.tsx
│   │   ├── NavBar.tsx
│   │   ├── Footer.tsx
│   │   ├── CumulativeReturnChart.tsx
│   │   └── StatsCard.tsx
│   ├── lib/                    # Utilities
│   │   ├── api.ts              # API client
│   │   └── utils.ts            # Helper functions
│   ├── styles/
│   │   └── globals.css
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js
├── data/
│   └── raw/                    # Raw factor data files
│       ├── us_factors/
│       ├── sweden_factors/
│       └── uk_factors/
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 12+
- npm or yarn

### 1. Clone the Repository

```bash
git clone <repository-url>
cd OpenPayments
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and configure:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/global_factor_lab

# Data Directory
DATA_DIR=/path/to/OpenPayments/data

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Environment
ENVIRONMENT=development
```

### 3. Set Up the Database

Create a PostgreSQL database:

```bash
createdb global_factor_lab
```

Or using psql:

```sql
CREATE DATABASE global_factor_lab;
```

### 4. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

### 6. Load Factor Data

The ETL pipeline ingests factor data from local CSV/TXT files.

**Run the ETL:**

```bash
cd backend
python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml
```

This will:
- Create country and factor definition records
- Parse CSV files from `data/raw/`
- Load factor returns into the database

**ETL Output:**

```
INFO - Loaded configuration from ./etl/config/global_factor_sources.yaml
INFO - Initialized 8 factor definitions
INFO - Processing source: United States (US) - Ken French Data Library
INFO - Found 2 file(s) matching pattern
INFO - Parsed 48 return observations
INFO - Loaded 48 returns for US/MKT
...
INFO - ETL pipeline completed
```

### 7. Start the Backend

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 8. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 9. Start the Frontend

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

## Adding New Factor Data

### Step 1: Download Data

Manually download factor data files and place them in `data/raw/<country>/`

Example:
```
data/raw/germany_factors/german_factors.csv
```

### Step 2: Update Configuration

Edit `backend/etl/config/global_factor_sources.yaml` and add a new source:

```yaml
sources:
  - country_code: DE
    country_name: Germany
    region_group: Developed
    source_name: My Data Source
    frequency: Monthly
    currency: EUR
    file_pattern: "germany_factors/*.csv"
    parser: generic_csv
    factor_mappings:
      Market: MKT
      Size: SMB
      Value: HML
      Momentum: MOM
    skip_rows: 0
    date_column: date
    date_format: "%Y-%m-%d"
```

### Step 3: Add Factor Definitions (if new factors)

If your data includes factors not yet defined, add them to the `factor_definitions` section:

```yaml
factor_definitions:
  - code: NEW_FACTOR
    name: New Factor Name
    group: Factor Group
    description: Description of the factor
```

### Step 4: Run ETL

```bash
cd backend
python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml
```

### Step 5: Verify

Check the API:
```bash
curl http://localhost:8000/api/countries
curl http://localhost:8000/api/countries/DE/factors
```

## API Endpoints

### Countries

- `GET /api/countries` - List all countries
- `GET /api/countries/{code}` - Get country details
- `GET /api/countries/{code}/factors` - List factors for a country

### Factors

- `GET /api/countries/{code}/factor/{factorCode}/timeseries` - Get time series
- `GET /api/countries/{code}/factor/{factorCode}/stats` - Get statistics
- `GET /api/countries/{code}/factors/comparison` - Compare multiple factors
- `GET /api/countries/{code}/correlation` - Get correlation matrix

### Cross-Country

- `GET /api/factors/{factorCode}/cross_country` - Cross-country performance
- `GET /api/factors/{factorCode}/heatmap` - Performance heatmap
- `GET /api/factors/{factorCode}/cross_country_correlation` - Cross-country correlations

## Database Schema

### Tables

**country**
- `id`: Primary key
- `code`: Country code (e.g., "US", "SE")
- `name`: Country name
- `region_group`: Region classification

**factor_definition**
- `id`: Primary key
- `code`: Factor code (e.g., "MKT", "HML")
- `name`: Factor name
- `group`: Factor group (e.g., "Value", "Momentum")
- `description`: Text description

**factor_series**
- `id`: Primary key
- `country_id`: Foreign key to country
- `factor_definition_id`: Foreign key to factor_definition
- `source_name`: Data source name
- `frequency`: "Daily" or "Monthly"
- `start_date`, `end_date`: Data range
- `currency`: Currency code

**factor_return**
- `id`: Primary key
- `factor_series_id`: Foreign key to factor_series
- `date`: Date of observation
- `return_value`: Factor return (decimal)

## Writing Custom Parsers

To support a new data format, create a parser class:

```python
# backend/etl/parsers/my_custom_parser.py

from .base_parser import BaseParser
import pandas as pd

class MyCustomParser(BaseParser):
    def parse(self, file_path: str, config: dict) -> pd.DataFrame:
        # Read file
        df = pd.read_csv(file_path)

        # Process and return DataFrame with columns:
        # - date (datetime)
        # - factor_code (str)
        # - return_value (float)

        return df
```

Register in `backend/etl/parsers/__init__.py`:

```python
from .my_custom_parser import MyCustomParser

PARSERS = {
    'my_custom': MyCustomParser,
    ...
}
```

Use in config:

```yaml
parser: my_custom
```

## Development

### Running Tests

```bash
# Backend tests (if implemented)
cd backend
pytest

# Frontend tests (if implemented)
cd frontend
npm test
```

### Code Style

Backend:
```bash
cd backend
black .
flake8 .
```

Frontend:
```bash
cd frontend
npm run lint
```

## Deployment

### Backend Deployment

1. Set up PostgreSQL on your VPS/cloud
2. Update `DATABASE_URL` in environment
3. Run migrations: `alembic upgrade head`
4. Load data: `python -m etl.load_factors ...`
5. Run with production ASGI server:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend Deployment

1. Build the Next.js app:

```bash
cd frontend
npm run build
```

2. Deploy to Vercel, Netlify, or serve with:

```bash
npm start
```

### Docker (Optional)

Create `Dockerfile` for backend:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Data Sources

This application uses publicly available academic factor datasets. Users must manually download data from:

- **Ken French Data Library**: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- **Swedish House of Finance**: https://www.houseoffinance.se/
- **AQR Capital**: https://www.aqr.com/Insights/Datasets

**Important**: Do not scrape or redistribute restricted data. Always consult original sources for licensing and terms of use.

## Disclaimer

This platform is for **educational and research purposes only**. Past performance does not guarantee future results. This is not investment advice. Consult a qualified financial advisor before making investment decisions.

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ for the quantitative finance community.