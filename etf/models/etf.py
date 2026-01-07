from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class PriceData:
    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int


@dataclass
class PerformanceMetrics:
    ticker: str
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    period_start: date
    period_end: date