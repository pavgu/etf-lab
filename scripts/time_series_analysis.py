#!/usr/bin/env python3
"""ETF time series analysis using new class-based architecture."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from etf.data.repository import PriceRepository
from etf.analysis.returns import ReturnsCalculator
from etf.analysis.risk import RiskCalculator


class TimeSeriesAnalyzer:
    """Time series analysis for ETFs."""
    
    def __init__(self):
        self.repo = PriceRepository()
        self.returns_calc = ReturnsCalculator()
        self.risk_calc = RiskCalculator()
    
    def load_etf_data(self, ticker: str) -> pd.DataFrame:
        """Load ETF data for analysis."""
        df = self.repo.load_prices(ticker)
        if df.empty:
            return df
        
        df.set_index('date', inplace=True)
        return df[['close']]
    
    def calculate_metrics(self, df: pd.DataFrame) -> dict:
        """Calculate performance metrics."""
        df_with_returns = self.returns_calc.cumulative_returns(df)
        returns = df_with_returns['daily_return'].dropna()
        
        # Use actual number of trading days for annualized return
        trading_days = len(returns)
        
        return {
            'total_return': df_with_returns['cumulative_return'].iloc[-1],
            'annualized_return': self.returns_calc.annualized_return(
                df_with_returns['cumulative_return'].iloc[-1], trading_days
            ),
            'volatility': self.risk_calc.volatility(returns),
            'sharpe_ratio': self.risk_calc.sharpe_ratio(returns),
            'max_drawdown': self.risk_calc.max_drawdown(df_with_returns['cumulative_return'])
        }
    
    def analyze_etf(self, ticker: str) -> tuple[pd.DataFrame, dict] | None:
        """Analyze single ETF."""
        print(f"\n=== {ticker} Analysis ===")
        
        df = self.load_etf_data(ticker)
        if df.empty:
            print(f"No data found for {ticker}")
            return None
        
        try:
            metrics = self.calculate_metrics(df)
            
            print(f"Period: {df.index[0].date()} to {df.index[-1].date()}")
            print(f"Total Return: {metrics['total_return']:.2%}")
            print(f"Annualized Return: {metrics['annualized_return']:.2%}")
            print(f"Volatility: {metrics['volatility']:.2%}")
            print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
            print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
            
            return df, metrics
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            return None
    
    def plot_comparison(self, tickers: list[str]):
        """Plot comparison of multiple ETFs."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        for ticker in tickers:
            try:
                df = self.load_etf_data(ticker)
                if not df.empty:
                    df_with_returns = self.returns_calc.cumulative_returns(df.reset_index())
                    df_with_returns = df_with_returns.set_index('date')
                    
                    ax1.plot(df_with_returns.index, df_with_returns['cumulative_return'], label=ticker)
                    ax2.plot(df_with_returns.index, 
                            df_with_returns['daily_return'].rolling(30).std() * np.sqrt(252), 
                            label=ticker)
            except Exception as e:
                print(f"Error plotting {ticker}: {e}")
                continue
        
        ax1.set_title('Cumulative Returns')
        ax1.set_ylabel('Return')
        ax1.legend()
        ax1.grid(True)
        
        ax2.set_title('30-Day Rolling Volatility')
        ax2.set_ylabel('Volatility')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        # Generate timestamped filename
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'etf_analysis_{timestamp}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    analyzer = TimeSeriesAnalyzer()
    tickers = ["SPY", "VEA", "VWO"]
    
    # Individual analysis
    results = {}
    for ticker in tickers:
        result = analyzer.analyze_etf(ticker)
        if result:
            _, metrics = result
            results[ticker] = metrics
    
    # Comparison plot
    if results:
        analyzer.plot_comparison(list(results.keys()))
        
        # Summary comparison
        print("\n=== Summary Comparison ===")
        comparison_df = pd.DataFrame(results).T
        print(comparison_df.round(4))
    else:
        print("\nNo successful analyses completed.")