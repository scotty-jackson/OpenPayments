"""
API endpoints for cross-country analytics and comparisons.
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db import get_db
from models import Country, FactorSeries, FactorDefinition, FactorReturn
import schemas
from .analytics_utils import (
    calculate_statistics,
    calculate_cumulative_returns,
    aggregate_returns_by_period
)

router = APIRouter()


@router.get("/factors/{factor_code}/cross_country",
           response_model=schemas.CrossCountryResponse)
async def get_cross_country_performance(
    factor_code: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    frequency: Optional[str] = "Monthly",
    db: Session = Depends(get_db)
):
    """
    Compare a factor's performance across countries.

    Args:
        factor_code: Factor code (e.g., "HML", "MOM")
        start_date: Optional start date
        end_date: Optional end date
        frequency: Data frequency (default: Monthly)

    Returns:
        Performance statistics and time series for each country
    """
    # Get factor definition
    factor_def = db.query(FactorDefinition).filter(
        FactorDefinition.code == factor_code.upper()
    ).first()

    if not factor_def:
        raise HTTPException(status_code=404, detail=f"Factor {factor_code} not found")

    # Get all factor series for this factor
    factor_series_list = db.query(FactorSeries, Country).join(
        Country,
        FactorSeries.country_id == Country.id
    ).filter(
        and_(
            FactorSeries.factor_definition_id == factor_def.id,
            FactorSeries.frequency == frequency
        )
    ).all()

    if not factor_series_list:
        raise HTTPException(
            status_code=404,
            detail=f"No {frequency} data found for factor {factor_code}"
        )

    countries_data = []

    for series, country in factor_series_list:
        # Get returns for this series
        returns_query = db.query(FactorReturn).filter(
            FactorReturn.factor_series_id == series.id
        )

        if start_date:
            returns_query = returns_query.filter(FactorReturn.date >= start_date)
        if end_date:
            returns_query = returns_query.filter(FactorReturn.date <= end_date)

        returns = returns_query.order_by(FactorReturn.date).all()

        if not returns:
            continue

        # Calculate statistics
        stats = calculate_statistics(
            returns=[r.return_value for r in returns],
            dates=[r.date for r in returns],
            frequency=series.frequency
        )

        # Calculate cumulative returns
        cumulative = calculate_cumulative_returns([r.return_value for r in returns])

        # Build time series
        returns_with_cumulative = [
            schemas.FactorReturnWithCumulative(
                date=ret.date,
                return_value=ret.return_value,
                cumulative_return=cum_ret
            )
            for ret, cum_ret in zip(returns, cumulative)
        ]

        countries_data.append(schemas.CountryFactorPerformance(
            country_code=country.code,
            country_name=country.name,
            annualized_return=stats['annualized_return'],
            annualized_volatility=stats['annualized_volatility'],
            sharpe_ratio=stats['sharpe_ratio'],
            start_date=returns[0].date,
            end_date=returns[-1].date,
            returns=returns_with_cumulative
        ))

    if not countries_data:
        raise HTTPException(status_code=404, detail="No data found for specified period")

    return schemas.CrossCountryResponse(
        factor_code=factor_def.code,
        factor_name=factor_def.name,
        countries=countries_data
    )


@router.get("/factors/{factor_code}/heatmap",
           response_model=schemas.HeatmapResponse)
async def get_factor_heatmap(
    factor_code: str,
    aggregation_period: str = Query("year", regex="^(year|decade)$"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Get heatmap data for a factor across countries and time periods.

    Args:
        factor_code: Factor code
        aggregation_period: "year" or "decade"
        start_date: Optional start date
        end_date: Optional end date

    Returns:
        Heatmap data with country x period cells
    """
    # Get factor definition
    factor_def = db.query(FactorDefinition).filter(
        FactorDefinition.code == factor_code.upper()
    ).first()

    if not factor_def:
        raise HTTPException(status_code=404, detail=f"Factor {factor_code} not found")

    # Get all factor series for this factor
    factor_series_list = db.query(FactorSeries, Country).join(
        Country,
        FactorSeries.country_id == Country.id
    ).filter(
        FactorSeries.factor_definition_id == factor_def.id
    ).all()

    if not factor_series_list:
        raise HTTPException(status_code=404, detail=f"No data found for factor {factor_code}")

    heatmap_data = []

    for series, country in factor_series_list:
        # Get returns
        returns_query = db.query(FactorReturn).filter(
            FactorReturn.factor_series_id == series.id
        )

        if start_date:
            returns_query = returns_query.filter(FactorReturn.date >= start_date)
        if end_date:
            returns_query = returns_query.filter(FactorReturn.date <= end_date)

        returns = returns_query.order_by(FactorReturn.date).all()

        if not returns:
            continue

        # Aggregate by period
        aggregated = aggregate_returns_by_period(
            returns=[(r.date, r.return_value) for r in returns],
            period=aggregation_period,
            frequency=series.frequency
        )

        # Add to heatmap data
        for period, return_value in aggregated.items():
            heatmap_data.append(schemas.HeatmapCell(
                country_code=country.code,
                period=period,
                return_value=return_value
            ))

    if not heatmap_data:
        raise HTTPException(status_code=404, detail="No data found for specified period")

    return schemas.HeatmapResponse(
        factor_code=factor_def.code,
        factor_name=factor_def.name,
        aggregation_period=aggregation_period,
        data=heatmap_data
    )


@router.get("/factors/{factor_code}/cross_country_correlation",
           response_model=schemas.CorrelationResponse)
async def get_cross_country_correlation(
    factor_code: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Calculate correlation matrix for a factor across countries.

    Args:
        factor_code: Factor code
        start_date: Optional start date
        end_date: Optional end date

    Returns:
        Correlation matrix showing how the factor correlates across countries
    """
    # Get factor definition
    factor_def = db.query(FactorDefinition).filter(
        FactorDefinition.code == factor_code.upper()
    ).first()

    if not factor_def:
        raise HTTPException(status_code=404, detail=f"Factor {factor_code} not found")

    # Get all factor series for this factor
    factor_series_list = db.query(FactorSeries, Country).join(
        Country,
        FactorSeries.country_id == Country.id
    ).filter(
        FactorSeries.factor_definition_id == factor_def.id
    ).all()

    # Collect returns by country
    country_returns = {}

    for series, country in factor_series_list:
        returns_query = db.query(FactorReturn).filter(
            FactorReturn.factor_series_id == series.id
        )

        if start_date:
            returns_query = returns_query.filter(FactorReturn.date >= start_date)
        if end_date:
            returns_query = returns_query.filter(FactorReturn.date <= end_date)

        returns = returns_query.order_by(FactorReturn.date).all()

        if returns:
            country_returns[country.code] = {
                r.date: r.return_value for r in returns
            }

    if len(country_returns) < 2:
        raise HTTPException(
            status_code=400,
            detail="Need at least 2 countries with data to calculate correlation"
        )

    # Calculate correlation matrix
    from .analytics_utils import calculate_correlation_matrix
    corr_matrix = calculate_correlation_matrix(country_returns)

    # Determine actual date range
    all_dates = set()
    for dates in country_returns.values():
        all_dates.update(dates.keys())

    return schemas.CorrelationResponse(
        country_code="CROSS_COUNTRY",
        start_date=min(all_dates),
        end_date=max(all_dates),
        correlation_matrix=schemas.CorrelationMatrix(
            factor_codes=list(corr_matrix.keys()),
            correlation_matrix=[[corr_matrix[c1][c2] for c2 in corr_matrix.keys()]
                              for c1 in corr_matrix.keys()]
        )
    )
