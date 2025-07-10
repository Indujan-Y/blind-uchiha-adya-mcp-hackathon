# MCP-STOCKANALYZER MCP Server – Demos and Payload Examples

## 🎥 Demo Video
- **MCP-STOCKANALYZER server setup, API Execution, and Features Testing**: [Watch Here](https://drive.google.com/file/d/1W54IUuQdH26UNR2E7oSe0aSP_qgbShYO/view?usp=sharing)

---

## 🎥 Credentials Gathering Video
- **How to get your NewsAPI key and configure MCP-STOCKANALYZER**: [Watch Here](
  
  
)

---

## 🔐 Credential JSON Payload
Example payload format for sending credentials to the MCP-STOCKANALYZER server (to be used in Client API payload):
```json
{
  "MCP-STOCKANALYZER": "YOUR_NEWSAPI_KEY"
}
```

---

## 🛠️ Example Tool Call Payload
Example payload for calling the `get_stock_news` tool:
```json
{
  "selected_servers": ["MCP-STOCKANALYZER"],
  "selected_server_credentials": {
    "MCP-STOCKANALYZER": "YOUR_NEWSAPI_KEY"
  },
  "selected_client": "MCP_CLIENT_OPENAI",
  "client_details": {
    "input": "Show me the latest news about AAPL",
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "get_stock_news",
          "parameters": {
            "symbol": "AAPL",
            "months": 1,
            "max_articles": 5
          }
        }
      }
    ],
    "chat_history": []
  }
}
```

--- 