import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from storage.db import get_connection


def load_etf_data(ticker: str) -> pd.DataFrame:
    con = get_connection()
    df = pd.read_sql(
        "SELECT date, close FROM prices WHERE ticker = ? ORDER BY date",
        con, params=[ticker]
    )
    con.close()
    
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    df['daily_return'] = df['close'].pct_change()
    df['cumulative_return'] = (1 + df['daily_return']).cumprod() - 1
    return df


def calculate_metrics(df: pd.DataFrame) -> dict:
    returns = df['daily_return'].dropna()
    
    return {
        'total_return': df['cumulative_return'].iloc[-1],
        'annualized_return': (1 + df['cumulative_return'].iloc[-1]) ** (252 / len(df)) - 1,
        'volatility': returns.std() * np.sqrt(252),
        'sharpe_ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)),
        'max_drawdown': (df['cumulative_return'] - df['cumulative_return'].cummax()).min()
    }


def analyze_etf(ticker: str):
    print(f"\n=== {ticker} Analysis ===")
    
    df = load_etf_data(ticker)
    if df.empty:
        print(f"No data found for {ticker}")
        return
    
    df = calculate_returns(df)
    metrics = calculate_metrics(df)
    
    print(f"Period: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"Total Return: {metrics['total_return']:.2%}")
    print(f"Annualized Return: {metrics['annualized_return']:.2%}")
    print(f"Volatility: {metrics['volatility']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
    
    return df, metrics


def plot_comparison(tickers: list[str]):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    for ticker in tickers:
        df = load_etf_data(ticker)
        if not df.empty:
            df = calculate_returns(df)
            ax1.plot(df.index, df['cumulative_return'], label=ticker)
            ax2.plot(df.index, df['daily_return'].rolling(30).std() * np.sqrt(252), label=ticker)
    
    ax1.set_title('Cumulative Returns')
    ax1.set_ylabel('Return')
    ax1.legend()
    ax1.grid(True)
    
    ax2.set_title('30-Day Rolling Volatility')
    ax2.set_ylabel('Volatility')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('etf_analysis.png', dpi=150, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    tickers = ["SPY", "VEA", "VWO"]
    
    # Individual analysis
    results = {}
    for ticker in tickers:
        df, metrics = analyze_etf(ticker)
        results[ticker] = metrics
    
    # Comparison plot
    plot_comparison(tickers)
    
    # Summary comparison
    print("\n=== Summary Comparison ===")
    comparison_df = pd.DataFrame(results).T
    print(comparison_df.round(4))