import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Dict, Optional


class ETFVisualizer:
    """ETF data visualization toolkit."""
    
    def __init__(self, figsize: tuple = (12, 8)):
        self.figsize = figsize
        plt.style.use('default')
    
    def plot_price_history(self, df: pd.DataFrame, ticker: str, save_path: Optional[str] = None):
        """Plot price history for a single ETF."""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(df['date'], df['close'], label=f'{ticker} Close Price', linewidth=2)
        ax.set_title(f'{ticker} Price History', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_returns_comparison(self, data: Dict[str, pd.DataFrame], save_path: Optional[str] = None):
        """Plot cumulative returns comparison for multiple ETFs."""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        for ticker, df in data.items():
            if 'cumulative_return' in df.columns:
                ax.plot(df['date'], df['cumulative_return'] * 100, 
                       label=ticker, linewidth=2)
        
        ax.set_title('Cumulative Returns Comparison', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Return (%)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_risk_return_scatter(self, metrics: Dict[str, Dict], save_path: Optional[str] = None):
        """Plot risk-return scatter chart."""
        fig, ax = plt.subplots(figsize=self.figsize)
        
        returns = [m['annualized_return'] * 100 for m in metrics.values()]
        volatilities = [m['volatility'] * 100 for m in metrics.values()]
        tickers = list(metrics.keys())
        
        scatter = ax.scatter(volatilities, returns, s=100, alpha=0.7)
        
        for i, ticker in enumerate(tickers):
            ax.annotate(ticker, (volatilities[i], returns[i]), 
                       xytext=(5, 5), textcoords='offset points')
        
        ax.set_title('Risk-Return Profile', fontsize=16, fontweight='bold')
        ax.set_xlabel('Volatility (%)')
        ax.set_ylabel('Annualized Return (%)')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_performance_dashboard(self, ticker: str, df: pd.DataFrame, metrics: Dict, 
                                 save_path: Optional[str] = None):
        """Create comprehensive performance dashboard."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # Price history
        ax1.plot(df['date'], df['close'], color='blue', linewidth=2)
        ax1.set_title(f'{ticker} Price History')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, alpha=0.3)
        
        # Cumulative returns
        if 'cumulative_return' in df.columns:
            ax2.plot(df['date'], df['cumulative_return'] * 100, color='green', linewidth=2)
            ax2.set_title('Cumulative Returns')
            ax2.set_ylabel('Return (%)')
            ax2.grid(True, alpha=0.3)
        
        # Rolling volatility
        if 'daily_return' in df.columns:
            rolling_vol = df['daily_return'].rolling(30).std() * np.sqrt(252) * 100
            ax3.plot(df['date'], rolling_vol, color='red', linewidth=2)
            ax3.set_title('30-Day Rolling Volatility')
            ax3.set_ylabel('Volatility (%)')
            ax3.grid(True, alpha=0.3)
        
        # Performance metrics bar chart
        metric_names = ['Total Return', 'Annual Return', 'Volatility', 'Sharpe Ratio']
        metric_values = [
            metrics.get('total_return', 0) * 100,
            metrics.get('annualized_return', 0) * 100,
            metrics.get('volatility', 0) * 100,
            metrics.get('sharpe_ratio', 0)
        ]
        
        bars = ax4.bar(metric_names, metric_values, color=['green', 'blue', 'red', 'orange'])
        ax4.set_title('Performance Metrics')
        ax4.set_ylabel('Value')
        ax4.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def save_chart(self, fig, filename: str):
        """Save chart with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"{filename}_{timestamp}.png"
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        return save_path