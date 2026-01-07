import pandas as pd
import numpy as np


class ReturnsCalculator:
    """Calculator for return metrics."""
    
    @staticmethod
    def daily_returns(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate daily returns."""
        if 'close' not in df.columns:
            raise ValueError("DataFrame missing required 'close' column")
        df = df.copy()
        df['daily_return'] = df['close'].pct_change()
        return df
    
    @staticmethod
    def cumulative_returns(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate cumulative returns."""
        df = df.copy()
        if 'daily_return' not in df.columns:
            df = ReturnsCalculator.daily_returns(df)
        # Handle NaN values in daily returns
        df['cumulative_return'] = (1 + df['daily_return'].fillna(0)).cumprod() - 1
        return df
    
    @staticmethod
    def annualized_return(cumulative_return: float, periods: int) -> float:
        """Calculate annualized return from cumulative return."""
        return (1 + cumulative_return) ** (252 / periods) - 1