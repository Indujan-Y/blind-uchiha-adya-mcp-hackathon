import yfinance as yf
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import numpy as np

class StockAnalyzer:
    def __init__(self, symbol: str, news_api_key: str):
        self.symbol = symbol.upper()
        self.stock = yf.Ticker(self.symbol)
        self.newsapi = NewsApiClient(api_key=news_api_key)

    def get_stock_details(self):
        info = self.stock.info
        details = {
            'symbol': self.symbol,
            'name': info.get('longName'),
            'current_price': info.get('currentPrice'),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'website': info.get('website'),
            'description': info.get('longBusinessSummary')
        }
        return details

    def get_stock_news(self, months=1, max_articles=10):
        query = self.symbol
        to_date = datetime.now()
        from_date = to_date - timedelta(days=30 * months)
        articles = self.newsapi.get_everything(
            q=query,
            from_param=from_date.strftime('%Y-%m-%d'),
            to=to_date.strftime('%Y-%m-%d'),
            language='en',
            sort_by='relevancy',
            page_size=max_articles
        )
        news = [{
            'title': a['title'],
            'description': a['description'],
            'url': a['url'],
            'published_at': a['publishedAt']
        } for a in articles['articles']]
        return news

    def get_similar_stocks(self):
        info = self.stock.info
        sector = info.get("sector")
        industry = info.get("industry")
        if not sector or not industry:
            return {"error": "No sector/industry info available"}
        suggestions = {
            ("Technology", "Consumer Electronics"): ["MSFT", "GOOGL", "AMZN"],
            ("Healthcare", "Biotechnology"): ["MRNA", "BNTX", "REGN"],
            ("Financial Services", "Banks—Diversified"): ["JPM", "BAC", "C"]
        }
        peers = suggestions.get((sector, industry), [])
        if not peers:
            return {"message": "No predefined peers found for this industry"}
        return peers

    def get_detailed_analysis(self):
        hist = self.stock.history(period="6mo")
        if hist.empty:
            return {"error": "No historical data available"}
        hist['SMA20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA50'] = hist['Close'].rolling(window=50).mean()
        latest = hist.iloc[-1]
        price = latest['Close']
        sma20 = latest['SMA20']
        sma50 = latest['SMA50']
        recommendation = "HOLD"
        rationale = "No clear trend."
        if price > sma20 > sma50:
            recommendation = "BUY"
            rationale = "Price is above short and medium-term averages. Uptrend."
        elif price < sma20 < sma50:
            recommendation = "SELL"
            rationale = "Price is below short and medium-term averages. Downtrend."
        analysis = {
            'current_price': price,
            'SMA20': sma20,
            'SMA50': sma50,
            'recommendation': recommendation,
            'rationale': rationale
        }
        return analysis 