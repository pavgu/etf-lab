# ETF Analysis Lab

A Python-based ETF (Exchange-Traded Fund) analysis toolkit for ingesting, storing, and analyzing financial data from Yahoo Finance.

## Features

- **Data Ingestion**: Fetch ETF price data from Yahoo Finance with incremental updates
- **Multiple Universes**: Support for US ETFs and European UCITS
- **Performance Analysis**: Calculate returns, volatility, Sharpe ratio, and maximum drawdown
- **Database Storage**: Efficient DuckDB storage with automatic schema management
- **Class-Based Architecture**: Modular, testable, and extensible design

## Project Structure

```
etf-lab/
├── etf/                    # Main package
│   ├── data/              # Data access layer
│   │   ├── ingestion.py   # Yahoo Finance data fetching
│   │   └── repository.py  # Database operations
│   ├── analysis/          # Analysis modules
│   │   ├── returns.py     # Return calculations
│   │   ├── risk.py        # Risk metrics
│   │   └── performance.py # Performance analysis
│   ├── models/            # Data models
│   │   └── etf.py         # ETF data structures
│   └── visualization/     # Plotting utilities
├── scripts/               # CLI scripts
│   ├── ingest.py         # Data ingestion
│   └── analyze.py        # Performance analysis
├── storage/              # Database layer
│   ├── db.py            # Database connection
│   └── schema.py        # Database schema
└── data/                # Data files
    └── universes/       # ETF universe definitions
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd etf-lab
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install yfinance pandas duckdb matplotlib numpy
```

## Usage

### Data Ingestion

Ingest ETF data from predefined universes:

```bash
# Ingest US ETFs (200 tickers)
python scripts/ingest.py --us

# Ingest European UCITS ETFs
python scripts/ingest.py --ucits

# Full reload (re-download all historical data)
python scripts/ingest.py --us --full

# Default tickers (SPY, VEA, VWO)
python scripts/ingest.py
```

### Performance Analysis

Analyze ETF performance metrics:

```bash
python scripts/analyze.py
```

### Programmatic Usage

```python
from etf.data.ingestion import YahooFinanceIngester
from etf.analysis.performance import PerformanceAnalyzer

# Ingest data
ingester = YahooFinanceIngester()
ingester.ingest_tickers(["SPY", "VTI"], incremental=True)

# Analyze performance
analyzer = PerformanceAnalyzer()
metrics = analyzer.analyze_etf("SPY")

print(f"Total Return: {metrics.total_return:.2%}")
print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
```

## Key Classes

### Data Layer
- **`YahooFinanceIngester`**: Fetches data from Yahoo Finance with error handling
- **`PriceRepository`**: Manages database operations with proper connection handling

### Analysis Layer
- **`ReturnsCalculator`**: Calculates daily and cumulative returns
- **`RiskCalculator`**: Computes volatility, Sharpe ratio, and maximum drawdown
- **`PerformanceAnalyzer`**: Orchestrates complete ETF analysis

### Models
- **`PriceData`**: Price data structure
- **`PerformanceMetrics`**: Analysis results container

## Features

### Incremental Data Loading
- Only downloads new data since last update
- Automatic detection of existing data
- Configurable rate limiting for API calls

### Error Handling
- Robust error handling for network failures
- Database connection management with proper cleanup
- Input validation for all operations

### Performance Metrics
- Total and annualized returns
- Volatility (annualized)
- Sharpe ratio
- Maximum drawdown
- Configurable risk-free rate

## Data Sources

- **US ETFs**: 200 core ETFs covering major asset classes
- **UCITS ETFs**: European-domiciled ETFs for global investors
- **Yahoo Finance**: Real-time and historical price data

## Database

Uses DuckDB for efficient storage:
- Automatic schema creation
- UPSERT operations for data updates
- Optimized for analytical queries

## Contributing

1. Follow the existing class-based architecture
2. Add proper error handling and input validation
3. Include type hints for all functions
4. Test with both US and UCITS universes

## License

MIT License - see LICENSE file for details.