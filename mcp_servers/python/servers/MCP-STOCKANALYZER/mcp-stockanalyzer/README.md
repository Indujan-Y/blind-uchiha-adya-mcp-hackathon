# mcp-stockanalyzer MCP server

MCP server to analyze stocks, fetch details, news, and provide recommendations.

## Features

- Fetch stock details (price, market cap, PE ratio, etc.)
- Get recent news about a stock
- Find similar stocks by sector/industry
- Analyze stock trends and get BUY/SELL/HOLD recommendations

## Example prompts

- Get details for AAPL
- Show me the latest news about TSLA
- Recommend similar stocks to MSFT
- Should I buy or sell GOOGL?

## Quickstart

### Install

This MCP server requires Python 3.10+ and the following dependencies:
- yfinance
- newsapi-python
- numpy
- mcp
- fastapi

Install dependencies:

```bash
pip install yfinance newsapi-python numpy mcp fastapi
```

### Usage

To run the server:

```bash
uv run mcp-stockanalyzer
```

## Development

- The main logic is in `src/mcp_stockanalyzer/`.
- Tools are defined in `tools_stock.py`.
- Stock analysis logic is in `stock.py`.

---

For more details, see the code and docstrings in each file. 