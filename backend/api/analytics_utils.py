"""
Utility functions for calculating factor analytics.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import date
from collections import defaultdict


def calculate_cumulative_returns(returns: List[float]) -> List[float]:
    """
    Calculate cumulative returns from a series of period returns.

    Args:
        returns: List of period returns (as decimals)

    Returns:
        List of cumulative returns (indexed to 100 at start)
    """
    cumulative = [100.0]
    for ret in returns:
        cumulative.append(cumulative[-1] * (1 + ret))

    return cumulative[1:]  # Skip initial 100


def calculate_statistics(
    returns: List[float],
    dates: List[date],
    frequency: str = "Monthly"
) -> Dict:
    """
    Calculate summary statistics for a return series.

    Args:
        returns: List of period returns (as decimals)
        dates: List of corresponding dates
        frequency: "Daily" or "Monthly"

    Returns:
        Dictionary of statistics
    """
    if not returns:
        return {}

    returns_arr = np.array(returns)

    # Determine annualization factor
    if frequency == "Daily":
        periods_per_year = 252
    elif frequency == "Monthly":
        periods_per_year = 12
    else:
        periods_per_year = 12  # Default

    # Annualized return
    mean_return = np.mean(returns_arr)
    annualized_return = (1 + mean_return) ** periods_per_year - 1

    # Annualized volatility
    volatility = np.std(returns_arr, ddof=1)
    annualized_volatility = volatility * np.sqrt(periods_per_year)

    # Sharpe ratio (assuming 0 risk-free rate for simplicity)
    sharpe_ratio = annualized_return / annualized_volatility if annualized_volatility > 0 else None

    # Max drawdown
    cumulative = calculate_cumulative_returns(returns)
    running_max = np.maximum.accumulate(cumulative)
    drawdowns = (cumulative - running_max) / running_max
    max_drawdown = np.min(drawdowns) if len(drawdowns) > 0 else None

    # Best and worst year (if we have enough data)
    best_year = None
    worst_year = None

    if frequency == "Monthly" and len(returns) >= 12:
        # Group by year
        yearly_returns = defaultdict(list)
        for ret, dt in zip(returns, dates):
            yearly_returns[dt.year].append(ret)

        # Calculate annual returns
        annual_perf = {}
        for year, year_rets in yearly_returns.items():
            if len(year_rets) >= 6:  # At least 6 months of data
                annual_ret = np.prod([1 + r for r in year_rets]) - 1
                annual_perf[year] = annual_ret

        if annual_perf:
            best_year_num = max(annual_perf, key=annual_perf.get)
            worst_year_num = min(annual_perf, key=annual_perf.get)

            best_year = {
                'year': best_year_num,
                'return': annual_perf[best_year_num]
            }
            worst_year = {
                'year': worst_year_num,
                'return': annual_perf[worst_year_num]
            }

    return {
        'annualized_return': annualized_return,
        'annualized_volatility': annualized_volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'best_year': best_year,
        'worst_year': worst_year
    }


def calculate_correlation_matrix(
    factor_returns: Dict[str, Dict[date, float]]
) -> Dict[str, Dict[str, float]]:
    """
    Calculate correlation matrix for multiple factors/countries.

    Args:
        factor_returns: Dict mapping factor/country code to {date: return} dict

    Returns:
        Nested dict representing correlation matrix
    """
    # Get common dates
    all_dates = set(factor_returns[list(factor_returns.keys())[0]].keys())
    for dates in factor_returns.values():
        all_dates &= set(dates.keys())

    common_dates = sorted(all_dates)

    if len(common_dates) < 2:
        # Not enough common observations
        return {}

    # Build aligned return matrix
    codes = list(factor_returns.keys())
    return_matrix = []

    for code in codes:
        code_returns = [factor_returns[code][dt] for dt in common_dates]
        return_matrix.append(code_returns)

    # Calculate correlation
    return_matrix = np.array(return_matrix)
    corr_matrix = np.corrcoef(return_matrix)

    # Convert to nested dict
    result = {}
    for i, code1 in enumerate(codes):
        result[code1] = {}
        for j, code2 in enumerate(codes):
            result[code1][code2] = float(corr_matrix[i, j])

    return result


def aggregate_returns_by_period(
    returns: List[Tuple[date, float]],
    period: str,
    frequency: str = "Monthly"
) -> Dict[str, float]:
    """
    Aggregate returns by time period (year or decade).

    Args:
        returns: List of (date, return_value) tuples
        period: "year" or "decade"
        frequency: Data frequency

    Returns:
        Dict mapping period label to aggregated return
    """
    period_returns = defaultdict(list)

    for dt, ret in returns:
        if period == "year":
            period_key = str(dt.year)
        elif period == "decade":
            decade = (dt.year // 10) * 10
            period_key = f"{decade}s"
        else:
            period_key = str(dt.year)

        period_returns[period_key].append(ret)

    # Calculate aggregated return for each period
    result = {}
    for period_key, rets in period_returns.items():
        # Compound returns
        if frequency == "Monthly":
            # Annualize if we have at least 6 months
            if len(rets) >= 6:
                compound = np.prod([1 + r for r in rets])
                if period == "year":
                    # Already annual
                    result[period_key] = compound - 1
                else:
                    # Annualize for decade
                    n_years = len(rets) / 12.0
                    if n_years > 0:
                        result[period_key] = compound ** (1.0 / n_years) - 1
        else:
            # Simple compounding
            compound = np.prod([1 + r for r in rets]) - 1
            result[period_key] = compound

    return result
