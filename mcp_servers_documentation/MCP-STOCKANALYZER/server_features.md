# MCP-STOCKANALYZER MCP Server Overview

## What is the MCP-STOCKANALYZER MCP Server?
The MCP-STOCKANALYZER MCP Server is a connector that enables seamless interaction with stock market data and news using the yfinance and NewsAPI APIs.

---

## Key Features
- ✅ Fetch stock details (price, market cap, PE ratio, etc.)
- ✅ Retrieve recent news about a stock
- ✅ Find similar stocks by sector/industry
- ✅ Analyze stock trends and get BUY/SELL/HOLD recommendations

---

## Capabilities
| Capability           | Description                                       |
|----------------------|---------------------------------------------------|
| Stock Details        | Get price, market cap, PE ratio, sector, etc.     |
| Stock News           | Fetch recent news articles for a stock            |
| Similar Stocks       | Suggest stocks in the same sector/industry        |
| Stock Analysis       | Analyze trends and recommend BUY/SELL/HOLD        |

---

## Supported APIs
- Yahoo Finance (via yfinance)
- NewsAPI (https://newsapi.org/)

---

## Security Notes
- Requires a valid NewsAPI key for news features
- No persistent storage of credentials; API key is passed per request
- All communications should be secured over HTTPS

---

## Integration Use Cases
- Financial dashboards
- Automated trading assistants
- Market research tools
- Portfolio analysis and reporting 