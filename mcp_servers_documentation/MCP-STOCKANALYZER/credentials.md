# MCP-STOCKANALYZER MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the MCP-STOCKANALYZER MCP Server.

---

## Credential Format
```json
{
  "MCP-STOCKANALYZER": "YOUR_NEWSAPI_KEY"
}
```

- Replace `YOUR_NEWSAPI_KEY` with your actual NewsAPI key from https://newsapi.org/.
- The API key is required for all news-related features.
- Credentials are passed per request and are not stored on the server. 