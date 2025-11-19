"""
Pydantic schemas for API request/response models.
"""
from datetime import date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Country Schemas
class CountryBase(BaseModel):
    code: str
    name: str
    region_group: Optional[str] = None


class Country(CountryBase):
    id: int
    factor_count: Optional[int] = 0

    class Config:
        from_attributes = True


class CountryDetail(Country):
    available_frequencies: List[str] = []


# Factor Definition Schemas
class FactorDefinitionBase(BaseModel):
    code: str
    name: str
    group: str
    description: Optional[str] = None


class FactorDefinition(FactorDefinitionBase):
    id: int

    class Config:
        from_attributes = True


# Factor Series Schemas
class FactorSeriesBase(BaseModel):
    source_name: str
    frequency: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    currency: Optional[str] = None


class FactorSeries(FactorSeriesBase):
    id: int
    country_id: int
    factor_definition_id: int
    factor_definition: Optional[FactorDefinition] = None

    class Config:
        from_attributes = True


class FactorSeriesWithDefinition(FactorSeries):
    factor_code: str
    factor_name: str
    factor_group: str


# Factor Return Schemas
class FactorReturn(BaseModel):
    date: date
    return_value: float

    class Config:
        from_attributes = True


class FactorReturnWithCumulative(FactorReturn):
    cumulative_return: Optional[float] = None


# Time Series Response
class TimeSeriesResponse(BaseModel):
    factor_code: str
    factor_name: str
    country_code: str
    frequency: str
    returns: List[FactorReturnWithCumulative]


# Statistics Schemas
class FactorStats(BaseModel):
    factor_code: str
    factor_name: str
    country_code: str
    annualized_return: Optional[float] = None
    annualized_volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    best_year: Optional[Dict[str, Any]] = None
    worst_year: Optional[Dict[str, Any]] = None
    observation_count: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# Cross-Country Comparison
class CountryFactorPerformance(BaseModel):
    country_code: str
    country_name: str
    annualized_return: Optional[float] = None
    annualized_volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    returns: Optional[List[FactorReturnWithCumulative]] = None


class CrossCountryResponse(BaseModel):
    factor_code: str
    factor_name: str
    countries: List[CountryFactorPerformance]


# Correlation Matrix
class CorrelationMatrix(BaseModel):
    factor_codes: List[str]
    correlation_matrix: List[List[float]]


class CorrelationResponse(BaseModel):
    country_code: str
    start_date: date
    end_date: date
    correlation_matrix: CorrelationMatrix


# Heatmap Response
class HeatmapCell(BaseModel):
    country_code: str
    period: str
    return_value: float


class HeatmapResponse(BaseModel):
    factor_code: str
    factor_name: str
    aggregation_period: str
    data: List[HeatmapCell]


# Factor Comparison within Country
class FactorComparisonResponse(BaseModel):
    country_code: str
    start_date: date
    end_date: date
    factors: List[TimeSeriesResponse]
