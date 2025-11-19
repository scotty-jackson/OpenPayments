"""
API endpoints for factor-related queries and time series data.
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
    calculate_correlation_matrix
)

router = APIRouter()


@router.get("/countries/{country_code}/factor/{factor_code}/timeseries",
           response_model=schemas.TimeSeriesResponse)
async def get_factor_timeseries(
    country_code: str,
    factor_code: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    frequency: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get time series data for a specific factor in a country.

    Args:
        country_code: Country code (e.g., "US", "SE")
        factor_code: Factor code (e.g., "MKT", "HML", "MOM")
        start_date: Optional start date filter
        end_date: Optional end date filter
        frequency: Optional frequency filter (if multiple available)

    Returns:
        Time series with dates, returns, and cumulative returns
    """
    # Get country
    country = db.query(Country).filter(Country.code == country_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country {country_code} not found")

    # Get factor definition
    factor_def = db.query(FactorDefinition).filter(
        FactorDefinition.code == factor_code.upper()
    ).first()
    if not factor_def:
        raise HTTPException(status_code=404, detail=f"Factor {factor_code} not found")

    # Get factor series
    query = db.query(FactorSeries).filter(
        and_(
            FactorSeries.country_id == country.id,
            FactorSeries.factor_definition_id == factor_def.id
        )
    )

    if frequency:
        query = query.filter(FactorSeries.frequency == frequency)

    factor_series = query.first()

    if not factor_series:
        raise HTTPException(
            status_code=404,
            detail=f"Factor series not found for {country_code}/{factor_code}"
        )

    # Get returns
    returns_query = db.query(FactorReturn).filter(
        FactorReturn.factor_series_id == factor_series.id
    )

    if start_date:
        returns_query = returns_query.filter(FactorReturn.date >= start_date)
    if end_date:
        returns_query = returns_query.filter(FactorReturn.date <= end_date)

    returns_query = returns_query.order_by(FactorReturn.date)
    returns = returns_query.all()

    if not returns:
        raise HTTPException(status_code=404, detail="No return data found for specified period")

    # Calculate cumulative returns
    cumulative_returns = calculate_cumulative_returns([r.return_value for r in returns])

    # Build response
    returns_with_cumulative = [
        schemas.FactorReturnWithCumulative(
            date=ret.date,
            return_value=ret.return_value,
            cumulative_return=cum_ret
        )
        for ret, cum_ret in zip(returns, cumulative_returns)
    ]

    return schemas.TimeSeriesResponse(
        factor_code=factor_def.code,
        factor_name=factor_def.name,
        country_code=country.code,
        frequency=factor_series.frequency,
        returns=returns_with_cumulative
    )


@router.get("/countries/{country_code}/factor/{factor_code}/stats",
           response_model=schemas.FactorStats)
async def get_factor_stats(
    country_code: str,
    factor_code: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    frequency: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get summary statistics for a factor.

    Args:
        country_code: Country code
        factor_code: Factor code
        start_date: Optional start date
        end_date: Optional end date
        frequency: Optional frequency filter

    Returns:
        Summary statistics including annualized return, volatility, Sharpe, max drawdown
    """
    # Get country
    country = db.query(Country).filter(Country.code == country_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country {country_code} not found")

    # Get factor definition
    factor_def = db.query(FactorDefinition).filter(
        FactorDefinition.code == factor_code.upper()
    ).first()
    if not factor_def:
        raise HTTPException(status_code=404, detail=f"Factor {factor_code} not found")

    # Get factor series
    query = db.query(FactorSeries).filter(
        and_(
            FactorSeries.country_id == country.id,
            FactorSeries.factor_definition_id == factor_def.id
        )
    )

    if frequency:
        query = query.filter(FactorSeries.frequency == frequency)

    factor_series = query.first()

    if not factor_series:
        raise HTTPException(
            status_code=404,
            detail=f"Factor series not found for {country_code}/{factor_code}"
        )

    # Get returns
    returns_query = db.query(FactorReturn).filter(
        FactorReturn.factor_series_id == factor_series.id
    )

    if start_date:
        returns_query = returns_query.filter(FactorReturn.date >= start_date)
    if end_date:
        returns_query = returns_query.filter(FactorReturn.date <= end_date)

    returns_query = returns_query.order_by(FactorReturn.date)
    returns = returns_query.all()

    if not returns:
        raise HTTPException(status_code=404, detail="No return data found")

    # Calculate statistics
    stats = calculate_statistics(
        returns=[r.return_value for r in returns],
        dates=[r.date for r in returns],
        frequency=factor_series.frequency
    )

    return schemas.FactorStats(
        factor_code=factor_def.code,
        factor_name=factor_def.name,
        country_code=country.code,
        annualized_return=stats['annualized_return'],
        annualized_volatility=stats['annualized_volatility'],
        sharpe_ratio=stats['sharpe_ratio'],
        max_drawdown=stats['max_drawdown'],
        best_year=stats.get('best_year'),
        worst_year=stats.get('worst_year'),
        observation_count=len(returns),
        start_date=returns[0].date,
        end_date=returns[-1].date
    )


@router.get("/countries/{country_code}/factors/comparison",
           response_model=schemas.FactorComparisonResponse)
async def compare_factors(
    country_code: str,
    factor_codes: List[str] = Query(...),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Compare multiple factors within a country.

    Args:
        country_code: Country code
        factor_codes: List of factor codes to compare
        start_date: Optional start date
        end_date: Optional end date

    Returns:
        Aligned time series for multiple factors
    """
    # Get country
    country = db.query(Country).filter(Country.code == country_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country {country_code} not found")

    factors = []

    for factor_code in factor_codes:
        try:
            # Get time series for each factor
            ts = await get_factor_timeseries(
                country_code=country_code,
                factor_code=factor_code,
                start_date=start_date,
                end_date=end_date,
                db=db
            )
            factors.append(ts)
        except HTTPException:
            continue

    if not factors:
        raise HTTPException(status_code=404, detail="No factor data found")

    # Determine common date range
    actual_start = max(f.returns[0].date for f in factors)
    actual_end = min(f.returns[-1].date for f in factors)

    return schemas.FactorComparisonResponse(
        country_code=country.code,
        start_date=actual_start,
        end_date=actual_end,
        factors=factors
    )


@router.get("/countries/{country_code}/correlation",
           response_model=schemas.CorrelationResponse)
async def get_country_correlation(
    country_code: str,
    factor_codes: List[str] = Query(...),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Calculate correlation matrix for factors within a country.

    Args:
        country_code: Country code
        factor_codes: List of factor codes
        start_date: Optional start date
        end_date: Optional end date

    Returns:
        Correlation matrix
    """
    # Get country
    country = db.query(Country).filter(Country.code == country_code.upper()).first()
    if not country:
        raise HTTPException(status_code=404, detail=f"Country {country_code} not found")

    # Collect returns for all factors
    factor_returns = {}

    for factor_code in factor_codes:
        factor_def = db.query(FactorDefinition).filter(
            FactorDefinition.code == factor_code.upper()
        ).first()

        if not factor_def:
            continue

        factor_series = db.query(FactorSeries).filter(
            and_(
                FactorSeries.country_id == country.id,
                FactorSeries.factor_definition_id == factor_def.id
            )
        ).first()

        if not factor_series:
            continue

        returns_query = db.query(FactorReturn).filter(
            FactorReturn.factor_series_id == factor_series.id
        )

        if start_date:
            returns_query = returns_query.filter(FactorReturn.date >= start_date)
        if end_date:
            returns_query = returns_query.filter(FactorReturn.date <= end_date)

        returns = returns_query.order_by(FactorReturn.date).all()

        if returns:
            factor_returns[factor_code.upper()] = {
                r.date: r.return_value for r in returns
            }

    if len(factor_returns) < 2:
        raise HTTPException(
            status_code=400,
            detail="Need at least 2 factors with data to calculate correlation"
        )

    # Calculate correlation matrix
    corr_matrix = calculate_correlation_matrix(factor_returns)

    # Determine actual date range
    all_dates = set()
    for dates in factor_returns.values():
        all_dates.update(dates.keys())

    return schemas.CorrelationResponse(
        country_code=country.code,
        start_date=min(all_dates),
        end_date=max(all_dates),
        correlation_matrix=schemas.CorrelationMatrix(
            factor_codes=list(corr_matrix.keys()),
            correlation_matrix=[[corr_matrix[f1][f2] for f2 in corr_matrix.keys()]
                              for f1 in corr_matrix.keys()]
        )
    )
