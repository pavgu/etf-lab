#!/usr/bin/env python3
"""Rank and visualize top ETFs by risk-adjusted return metrics."""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import matplotlib.pyplot as plt
import argparse
from datetime import datetime, timedelta
from etf.data.repository import PriceRepository
from etf.analysis.returns import ReturnsCalculator
from etf.analysis.risk import RiskCalculator
from storage.db import get_connection

def get_isin(ticker: str) -> str:
    """Get ISIN for ticker from metadata."""
    con = get_connection()
    try:
        result = con.execute(
            "SELECT isin FROM etf_metadata WHERE ticker = ?", [ticker]
        ).fetchone()
        return result[0] if result and result[0] else ""
    finally:
        con.close()

def get_metadata(ticker: str) -> tuple:
    """Get ISIN and description for ticker."""
    con = get_connection()
    try:
        result = con.execute(
            "SELECT isin, description FROM etf_metadata WHERE ticker = ?", [ticker]
        ).fetchone()
        return (result[0] if result and result[0] else "", 
                result[1] if result and result[1] else "") if result else ("", "")
    finally:
        con.close()

def main():
    parser = argparse.ArgumentParser(description='Rank ETFs by risk-adjusted metrics')
    parser.add_argument('--months', type=int, help='Analysis period in months (e.g., 12, 24, 36)')
    args = parser.parse_args()
    
    repo = PriceRepository()
    returns_calc = ReturnsCalculator()
    risk_calc = RiskCalculator()
    
    tickers = repo.get_available_tickers()
    if not tickers:
        print("No data found. Run ingestion first.")
        return
    
    print(f"Analyzing {len(tickers)} ETFs...")
    if args.months:
        print(f"Period: Last {args.months} months")
    
    results = []
    for ticker in tickers:
        try:
            df = repo.load_prices(ticker)
            if len(df) < 2:
                continue
            
            # Filter by period if specified
            if args.months:
                cutoff_date = pd.Timestamp(datetime.now() - timedelta(days=args.months * 30.44))
                df = df[df['date'] >= cutoff_date].copy()
                if len(df) < 2:
                    continue
            
            df = returns_calc.cumulative_returns(df)
            returns = df['daily_return'].dropna()
            
            if len(returns) == 0:
                continue
            
            # Calculate analysis period in months
            days = (df['date'].max() - df['date'].min()).days
            months = round(days / 30.44)
            
            isin, description = get_metadata(ticker)
            bar_label = ticker
            legend_label = f"{ticker} - {description} ({isin}, {months}m)" if description else f"{ticker} ({isin}, {months}m)"
            
            results.append({
                'ticker': ticker,
                'bar_label': bar_label,
                'legend_label': legend_label,
                'sharpe': risk_calc.sharpe_ratio(returns),
                'sortino': risk_calc.sortino_ratio(returns),
                'calmar': risk_calc.calmar_ratio(df['cumulative_return'], returns)
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue
    
    if not results:
        print("No valid results.")
        return
    
    df_results = pd.DataFrame(results)
    
    # Get top 5 for each metric
    top_sharpe = df_results.nlargest(5, 'sharpe')
    top_sortino = df_results.nlargest(5, 'sortino')
    top_calmar = df_results.nlargest(5, 'calmar')
    
    # Print results
    print("\n=== Top 5 by Sharpe Ratio ===")
    print(top_sharpe[['ticker', 'sharpe']].to_string(index=False))
    
    print("\n=== Top 5 by Sortino Ratio ===")
    print(top_sortino[['ticker', 'sortino']].to_string(index=False))
    
    print("\n=== Top 5 by Calmar Ratio ===")
    print(top_calmar[['ticker', 'calmar']].to_string(index=False))
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directory
    output_dir = project_root / "output" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create ratio comparison chart
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    axes[0].barh(top_sharpe['bar_label'], top_sharpe['sharpe'])
    axes[0].set_xlabel('Sharpe Ratio')
    axes[0].set_title('Top 5 ETFs by Sharpe Ratio')
    axes[0].invert_yaxis()
    
    axes[1].barh(top_sortino['bar_label'], top_sortino['sortino'])
    axes[1].set_xlabel('Sortino Ratio')
    axes[1].set_title('Top 5 ETFs by Sortino Ratio')
    axes[1].invert_yaxis()
    
    axes[2].barh(top_calmar['bar_label'], top_calmar['calmar'])
    axes[2].set_xlabel('Calmar Ratio')
    axes[2].set_title('Top 5 ETFs by Calmar Ratio')
    axes[2].invert_yaxis()
    
    plt.tight_layout()
    filename = output_dir / 'top_etfs_ratios.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nRatio chart saved: {filename}")
    
    # Create cumulative returns charts for each ratio
    for ratio_name, top_df in [('sharpe', top_sharpe), ('sortino', top_sortino), ('calmar', top_calmar)]:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for _, row in top_df.iterrows():
            ticker = row['ticker']
            df = repo.load_prices(ticker)
            
            if args.months:
                cutoff_date = pd.Timestamp(datetime.now() - timedelta(days=args.months * 30.44))
                df = df[df['date'] >= cutoff_date].copy()
            
            df = returns_calc.cumulative_returns(df)
            ax.plot(df['date'], df['cumulative_return'] * 100, label=row['legend_label'], linewidth=2)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Return (%)')
        ax.set_title(f'Cumulative Returns - Top 5 by {ratio_name.capitalize()} Ratio')
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = output_dir / f'returns_{ratio_name}.png'
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Returns chart saved: {filename}")
    
    plt.show()

if __name__ == "__main__":
    main()
