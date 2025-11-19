"""
API endpoints for country-related queries.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Country, FactorSeries, FactorDefinition
import schemas

router = APIRouter()


@router.get("/countries", response_model=List[schemas.CountryDetail])
async def list_countries(db: Session = Depends(get_db)):
    """
    Get list of all countries with available factor data.

    Returns:
        List of countries with metadata including factor count and available frequencies
    """
    countries = db.query(Country).all()

    result = []
    for country in countries:
        # Count factor series
        factor_count = db.query(FactorSeries).filter(
            FactorSeries.country_id == country.id
        ).count()

        # Get available frequencies
        frequencies = db.query(FactorSeries.frequency).filter(
            FactorSeries.country_id == country.id
        ).distinct().all()
        available_frequencies = [f[0] for f in frequencies]

        result.append(schemas.CountryDetail(
            id=country.id,
            code=country.code,
            name=country.name,
            region_group=country.region_group,
            factor_count=factor_count,
            available_frequencies=available_frequencies
        ))

    return result


@router.get("/countries/{country_code}", response_model=schemas.CountryDetail)
async def get_country(country_code: str, db: Session = Depends(get_db)):
    """
    Get details for a specific country.

    Args:
        country_code: Country code (e.g., "US", "SE", "UK")

    Returns:
        Country details with factor count and available frequencies
    """
    country = db.query(Country).filter(Country.code == country_code.upper()).first()

    if not country:
        raise HTTPException(status_code=404, detail=f"Country {country_code} not found")

    # Count factor series
    factor_count = db.query(FactorSeries).filter(
        FactorSeries.country_id == country.id
    ).count()

    # Get available frequencies
    frequencies = db.query(FactorSeries.frequency).filter(
        FactorSeries.country_id == country.id
    ).distinct().all()
    available_frequencies = [f[0] for f in frequencies]

    return schemas.CountryDetail(
        id=country.id,
        code=country.code,
        name=country.name,
        region_group=country.region_group,
        factor_count=factor_count,
        available_frequencies=available_frequencies
    )


@router.get("/countries/{country_code}/factors",
           response_model=List[schemas.FactorSeriesWithDefinition])
async def list_country_factors(country_code: str, db: Session = Depends(get_db)):
    """
    Get all factor series available for a country.

    Args:
        country_code: Country code (e.g., "US", "SE", "UK")

    Returns:
        List of factor series with their definitions
    """
    country = db.query(Country).filter(Country.code == country_code.upper()).first()

    if not country:
        raise HTTPException(status_code=404, detail=f"Country {country_code} not found")

    # Query factor series with definitions
    factor_series = db.query(FactorSeries, FactorDefinition).join(
        FactorDefinition,
        FactorSeries.factor_definition_id == FactorDefinition.id
    ).filter(
        FactorSeries.country_id == country.id
    ).all()

    result = []
    for series, definition in factor_series:
        result.append(schemas.FactorSeriesWithDefinition(
            id=series.id,
            country_id=series.country_id,
            factor_definition_id=series.factor_definition_id,
            source_name=series.source_name,
            frequency=series.frequency,
            start_date=series.start_date,
            end_date=series.end_date,
            currency=series.currency,
            factor_code=definition.code,
            factor_name=definition.name,
            factor_group=definition.group
        ))

    return result
