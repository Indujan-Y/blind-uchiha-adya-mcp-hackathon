from collections.abc import Sequence
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from .stock import StockAnalyzer
from .toolhandler import ToolHandler, CREDENTIALS_ARG

class StockDetailsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_stock_details")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get details for a stock symbol (price, market cap, PE ratio, etc.). Requires NewsAPI credentials in __credentials__.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL, TSLA)"},
                    CREDENTIALS_ARG: {"type": "string", "description": "NewsAPI key (required)"}
                },
                "required": ["symbol", CREDENTIALS_ARG]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        symbol = args.get("symbol")
        news_api_key = args.get(CREDENTIALS_ARG)
        if not symbol:
            raise RuntimeError("Missing required argument: symbol")
        if not news_api_key:
            raise RuntimeError(f"Missing required argument: {CREDENTIALS_ARG}")
        analyzer = StockAnalyzer(symbol, news_api_key)
        details = analyzer.get_stock_details()
        return [TextContent(type="text", text=str(details))]

class StockNewsToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_stock_news")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get recent news for a stock symbol. Requires NewsAPI credentials in __credentials__.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL, TSLA)"},
                    "months": {"type": "integer", "description": "How many months back to search", "default": 1},
                    "max_articles": {"type": "integer", "description": "Maximum number of articles", "default": 10},
                    CREDENTIALS_ARG: {"type": "string", "description": "NewsAPI key (required)"}
                },
                "required": ["symbol", CREDENTIALS_ARG]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        symbol = args.get("symbol")
        months = args.get("months", 1)
        max_articles = args.get("max_articles", 10)
        news_api_key = args.get(CREDENTIALS_ARG)
        if not symbol:
            raise RuntimeError("Missing required argument: symbol")
        if not news_api_key:
            raise RuntimeError(f"Missing required argument: {CREDENTIALS_ARG}")
        analyzer = StockAnalyzer(symbol, news_api_key)
        news = analyzer.get_stock_news(months=months, max_articles=max_articles)
        return [TextContent(type="text", text=str(news))]

class SimilarStocksToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_similar_stocks")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get similar stocks for a given symbol (same sector/industry). Requires NewsAPI credentials in __credentials__.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL, TSLA)"},
                    CREDENTIALS_ARG: {"type": "string", "description": "NewsAPI key (required)"}
                },
                "required": ["symbol", CREDENTIALS_ARG]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        symbol = args.get("symbol")
        news_api_key = args.get(CREDENTIALS_ARG)
        if not symbol:
            raise RuntimeError("Missing required argument: symbol")
        if not news_api_key:
            raise RuntimeError(f"Missing required argument: {CREDENTIALS_ARG}")
        analyzer = StockAnalyzer(symbol, news_api_key)
        peers = analyzer.get_similar_stocks()
        return [TextContent(type="text", text=str(peers))]

class StockAnalysisToolHandler(ToolHandler):
    def __init__(self):
        super().__init__("get_stock_analysis")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get a detailed analysis and recommendation (BUY/SELL/HOLD) for a stock symbol. Requires NewsAPI credentials in __credentials__.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock symbol (e.g., AAPL, TSLA)"},
                    CREDENTIALS_ARG: {"type": "string", "description": "NewsAPI key (required)"}
                },
                "required": ["symbol", CREDENTIALS_ARG]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        symbol = args.get("symbol")
        news_api_key = args.get(CREDENTIALS_ARG)
        if not symbol:
            raise RuntimeError("Missing required argument: symbol")
        if not news_api_key:
            raise RuntimeError(f"Missing required argument: {CREDENTIALS_ARG}")
        analyzer = StockAnalyzer(symbol, news_api_key)
        analysis = analyzer.get_detailed_analysis()
        return [TextContent(type="text", text=str(analysis))] 