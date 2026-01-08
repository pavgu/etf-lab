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
    
    @staticmethod
    def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
        """Calculate Sortino ratio (uses downside deviation)."""
        if returns.empty:
            return 0.0
        excess_returns = returns.mean() * 252 - risk_free_rate
        downside_returns = returns[returns < 0]
        downside_std = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 0 else 0.0
        return excess_returns / downside_std if downside_std > 0 else 0.0
    
    @staticmethod
    def calmar_ratio(cumulative_returns: pd.Series, returns: pd.Series) -> float:
        """Calculate Calmar ratio (annualized return / max drawdown)."""
        if returns.empty or cumulative_returns.empty:
            return 0.0
        annualized_return = returns.mean() * 252
        max_dd = abs(RiskCalculator.max_drawdown(cumulative_returns))
        return annualized_return / max_dd if max_dd > 0 else 0.0