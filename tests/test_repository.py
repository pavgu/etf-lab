import unittest
import pandas as pd
from etf.data.repository import PriceRepository


class TestPriceRepository(unittest.TestCase):
    
    def setUp(self):
        self.repo = PriceRepository()
    
    def test_save_prices_invalid_input(self):
        # Test non-DataFrame input
        with self.assertRaises(TypeError):
            self.repo.save_prices("not a dataframe")
    
    def test_save_prices_empty_dataframe(self):
        # Test empty DataFrame
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.repo.save_prices(empty_df)
    
    def test_save_prices_missing_columns(self):
        # Test DataFrame missing required columns
        df = pd.DataFrame({'wrong_col': [1, 2, 3]})
        with self.assertRaises(ValueError):
            self.repo.save_prices(df)
    
    def test_save_prices_valid_data(self):
        # Test valid DataFrame
        df = pd.DataFrame({
            'ticker': ['SPY'],
            'date': ['2023-01-01'],
            'close': [400.0],
            'open': [399.0],
            'high': [401.0],
            'low': [398.0],
            'adj_close': [400.0],
            'volume': [1000000]
        })
        # Should not raise any exception
        try:
            self.repo.save_prices(df)
        except Exception as e:
            self.fail(f"save_prices raised {e} unexpectedly")


if __name__ == '__main__':
    unittest.main()