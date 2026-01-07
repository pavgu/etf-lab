#!/usr/bin/env python3
"""ETF analysis script."""

import pandas as pd
from etf.data.repository import PriceRepository
from etf.analysis.performance import PerformanceAnalyzer


def main():
    repo = PriceRepository()
    analyzer = PerformanceAnalyzer()
    
    tickers = repo.get_available_tickers()
    if not tickers:
        print("No data found. Run ingestion first.")
        return
    
    print("=== ETF Performance Analysis ===\n")
    
    results = []
    for ticker in tickers:
        try:
            metrics = analyzer.analyze_etf(ticker)
            results.append({
                'Ticker': metrics.ticker,
                'Total Return': f"{metrics.total_return:.2%}",
                'Annual Return': f"{metrics.annualized_return:.2%}",
                'Volatility': f"{metrics.volatility:.2%}",
                'Sharpe Ratio': f"{metrics.sharpe_ratio:.2f}",
                'Max Drawdown': f"{metrics.max_drawdown:.2%}"
            })
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
    
    if results:
        df = pd.DataFrame(results)
        print(df.to_string(index=False))
    else:
        print("No successful analyses completed.")


if __name__ == "__main__":
    main()