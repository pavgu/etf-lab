#!/usr/bin/env python3
"""ETF visualization script."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from etf.data.repository import PriceRepository
from etf.analysis.returns import ReturnsCalculator
from etf.analysis.risk import RiskCalculator
from etf.visualization.charts import ETFVisualizer


def main():
    repo = PriceRepository()
    returns_calc = ReturnsCalculator()
    risk_calc = RiskCalculator()
    visualizer = ETFVisualizer()
    
    tickers = repo.get_available_tickers()
    if not tickers:
        print("No data found. Run ingestion first.")
        return
    
    print(f"Creating visualizations for {len(tickers)} ETFs...")
    
    # Prepare data for comparison charts
    etf_data = {}
    etf_metrics = {}
    
    for ticker in tickers[:5]:  # Limit to first 5 for readability
        df = repo.load_prices(ticker)
        if not df.empty and len(df) > 1:
            df = returns_calc.cumulative_returns(df)
            returns = df['daily_return'].dropna()
            
            if len(returns) == 0:
                continue
            
            etf_data[ticker] = df
            etf_metrics[ticker] = {
                'total_return': df['cumulative_return'].iloc[-1],
                'annualized_return': returns_calc.annualized_return(
                    df['cumulative_return'].iloc[-1], len(df)
                ),
                'volatility': risk_calc.volatility(returns),
                'sharpe_ratio': risk_calc.sharpe_ratio(returns)
            }
    
    if etf_data:
        # Create comparison charts
        print("Creating returns comparison chart...")
        fig1 = visualizer.plot_returns_comparison(etf_data)
        path1 = visualizer.save_chart(fig1, "etf_returns_comparison")
        print(f"Saved: {path1}")
        
        print("Creating risk-return scatter plot...")
        fig2 = visualizer.plot_risk_return_scatter(etf_metrics)
        path2 = visualizer.save_chart(fig2, "etf_risk_return_scatter")
        print(f"Saved: {path2}")
        
        # Create dashboard for first ETF
        first_ticker = list(etf_data.keys())[0]
        print(f"Creating performance dashboard for {first_ticker}...")
        fig3 = visualizer.plot_performance_dashboard(
            first_ticker, etf_data[first_ticker], etf_metrics[first_ticker]
        )
        path3 = visualizer.save_chart(fig3, f"etf_dashboard_{first_ticker}")
        print(f"Saved: {path3}")
        
        print("\nVisualization complete!")
    else:
        print("No valid ETF data found for visualization.")


if __name__ == "__main__":
    main()
