import pandas as pd
import numpy as np


class RiskCalculator:
    """Calculator for risk metrics."""
    
    @staticmethod
    def volatility(returns: pd.Series) -> float:
        """Calculate annualized volatility."""
        return returns.std() * np.sqrt(252)
    
    @staticmethod
    def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
        """Calculate Sharpe ratio."""
        excess_returns = returns.mean() * 252 - risk_free_rate
        vol = RiskCalculator.volatility(returns)
        return excess_returns / vol if vol > 0 else 0.0
    
    @staticmethod
    def max_drawdown(cumulative_returns: pd.Series) -> float:
        """Calculate maximum drawdown."""
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / (1 + peak)
        return drawdown.min()