import unittest
import pandas as pd
import numpy as np
from etf.analysis.risk import RiskCalculator


class TestRiskCalculator(unittest.TestCase):
    
    def test_volatility_empty_series(self):
        empty_series = pd.Series([], dtype=float)
        result = RiskCalculator.volatility(empty_series)
        self.assertEqual(result, 0.0)
    
    def test_sharpe_ratio_empty_series(self):
        empty_series = pd.Series([], dtype=float)
        result = RiskCalculator.sharpe_ratio(empty_series)
        self.assertEqual(result, 0.0)
    
    def test_max_drawdown_empty_series(self):
        empty_series = pd.Series([], dtype=float)
        result = RiskCalculator.max_drawdown(empty_series)
        self.assertEqual(result, 0.0)
    
    def test_max_drawdown_calculation(self):
        # Test with known values
        cumulative_returns = pd.Series([0.0, 0.1, 0.05, 0.15, 0.08])
        result = RiskCalculator.max_drawdown(cumulative_returns)
        # Should be negative (drawdown)
        self.assertLess(result, 0)


if __name__ == '__main__':
    unittest.main()