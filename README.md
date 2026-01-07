# ETF Analysis Lab

A Python-based ETF (Exchange-Traded Fund) analysis toolkit for ingesting, storing, and analyzing financial data from Yahoo Finance.

## Features

- **Data Ingestion**: Fetch ETF price data from Yahoo Finance with incremental updates
- **Multiple Universes**: Support for US ETFs and European UCITS
- **Performance Analysis**: Calculate returns, volatility, Sharpe ratio, and maximum drawdown
- **Database Storage**: Efficient DuckDB storage with automatic schema management
- **Class-Based Architecture**: Modular, testable, and extensible design
- **Robust Error Handling**: Comprehensive input validation and error management
- **Unit Testing**: Test coverage for critical components

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
│   ├── analyze.py        # Performance analysis
│   └── check_db.py       # Database inspection
├── storage/              # Database layer
│   ├── db.py            # Database connection
│   └── schema.py        # Database schema
├── tests/                # Unit tests
│   ├── test_repository.py
│   ├── test_risk.py
│   └── run_tests.py
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

4. Initialize database with ETF data:
```bash
# Ingest US ETFs (200 tickers)
python scripts/ingest.py --us

# Ingest European UCITS ETFs  
python scripts/ingest.py --ucits

# Or both at once
python scripts/ingest.py --us --ucits
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

### Database Inspection

Check database contents:

```bash
python scripts/check_db.py
```

### Exchange Analysis

Analyze which exchanges are represented:

```bash
python scripts/analyze_exchanges.py
```

### Running Tests

Run unit tests:

```bash
python tests/run_tests.py
```

### Programmatic Usage

```python
from etf.data.ingestion import YahooFinanceIngester
from etf.analysis.performance import PerformanceAnalyzer
from etf.visualization.charts import ETFVisualizer

# Ingest data
ingester = YahooFinanceIngester()
ingester.ingest_tickers(["SPY", "VTI"], incremental=True)

# Analyze performance
analyzer = PerformanceAnalyzer()
metrics = analyzer.analyze_etf("SPY")

# Create visualizations
visualizer = ETFVisualizer()
fig = visualizer.plot_performance_dashboard("SPY", data, metrics)
visualizer.save_chart(fig, "spy_dashboard")

print(f"Total Return: {metrics.total_return:.2%}")
print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
```

## Key Classes

### Data Layer
- **`YahooFinanceIngester`**: Fetches data from Yahoo Finance with error handling and rate limiting
- **`PriceRepository`**: Manages database operations with proper connection handling and input validation

### Analysis Layer
- **`ReturnsCalculator`**: Calculates daily and cumulative returns with edge case handling
- **`RiskCalculator`**: Computes volatility, Sharpe ratio, and maximum drawdown
- **`PerformanceAnalyzer`**: Orchestrates complete ETF analysis

### Models
- **`PriceData`**: Price data structure
- **`PerformanceMetrics`**: Analysis results container

### Visualization
- **`ETFVisualizer`**: Creates charts and performance dashboards

## Features

### Incremental Data Loading
- Only downloads new data since last update
- Automatic detection of existing data
- Configurable rate limiting for API calls
- Smart error handling for network failures

### Error Handling
- Comprehensive input validation
- Database connection management with proper cleanup
- Graceful handling of API failures
- Detailed logging for debugging

### Performance Metrics
- Total and annualized returns
- Volatility (annualized)
- Sharpe ratio with configurable risk-free rate
- Maximum drawdown using industry-standard formula

## Data Sources

- **US ETFs**: 200 core ETFs covering major asset classes (NYSE Arca, NASDAQ)
- **UCITS ETFs**: European-domiciled ETFs for global investors (LSE, Xetra)
- **Yahoo Finance**: Real-time and historical price data
- **4 Exchanges**: NYSE Arca, NASDAQ, London Stock Exchange, Xetra (Germany)

## Database

Uses DuckDB for efficient storage:
- Automatic schema creation
- UPSERT operations for data updates
- Optimized for analytical queries
- Proper connection management

## Testing

Unit tests cover:
- Input validation in repository methods
- Edge cases in risk calculations
- Error handling scenarios
- Data integrity checks

## Contributing

1. Follow the existing class-based architecture
2. Add proper error handling and input validation
3. Include type hints for all functions
4. Write unit tests for new functionality
5. Test with both US and UCITS universes

## License

MIT License - see LICENSE file for details.