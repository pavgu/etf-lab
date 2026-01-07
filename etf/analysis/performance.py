from etf.data.repository import PriceRepository
from etf.analysis.returns import ReturnsCalculator
from etf.analysis.risk import RiskCalculator
from etf.models.etf import PerformanceMetrics


class PerformanceAnalyzer:
    """ETF performance analyzer."""
    
    def __init__(self):
        self.repo = PriceRepository()
        self.returns_calc = ReturnsCalculator()
        self.risk_calc = RiskCalculator()
    
    def analyze_etf(self, ticker: str) -> PerformanceMetrics:
        """Perform complete performance analysis for an ETF."""
        df = self.repo.load_prices(ticker)
        if df.empty:
            raise ValueError(f"No data found for {ticker}")
        
        # Validate required columns
        required_cols = ['close', 'date']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        df = self.returns_calc.cumulative_returns(df)
        returns = df['daily_return'].dropna()
        
        return PerformanceMetrics(
            ticker=ticker,
            total_return=df['cumulative_return'].iloc[-1],
            annualized_return=self.returns_calc.annualized_return(df['cumulative_return'].iloc[-1], len(df)),
            volatility=self.risk_calc.volatility(returns),
            sharpe_ratio=self.risk_calc.sharpe_ratio(returns),
            max_drawdown=self.risk_calc.max_drawdown(df['cumulative_return']),
            period_start=df['date'].iloc[0].date(),
            period_end=df['date'].iloc[-1].date()
        )