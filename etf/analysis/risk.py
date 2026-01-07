import pandas as pd
import numpy as np


class RiskCalculator:
    """Calculator for risk metrics."""
    
    @staticmethod
    def volatility(returns: pd.Series) -> float:
        """Calculate annualized volatility."""
        if returns.empty:
            return 0.0
        return returns.std() * np.sqrt(252)
    
    @staticmethod
    def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
        """Calculate Sharpe ratio."""
        if returns.empty:
            return 0.0
        excess_returns = returns.mean() * 252 - risk_free_rate
        vol = RiskCalculator.volatility(returns)
        return excess_returns / vol if vol > 0 else 0.0
    
    @staticmethod
    def max_drawdown(cumulative_returns: pd.Series) -> float:
        """Calculate maximum drawdown."""
        if cumulative_returns.empty:
            return 0.0
        
        # Convert cumulative returns to wealth index (starting at 1)
        wealth_index = 1 + cumulative_returns
        peak = wealth_index.cummax()
        drawdown = (wealth_index - peak) / peak
        return drawdown.min()