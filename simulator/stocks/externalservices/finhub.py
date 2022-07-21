import finnhub
import core.settings as settings;
from datetime import datetime, timedelta

def lookup_stocks(data):
    finnhub_client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)
    return (finnhub_client.symbol_lookup(data))

def get_candle_stick_data(stock,resolution,days):
    finnhub_client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)
    now = datetime.now()
    delta = timedelta(days=days)
    prev = (int)((now - delta).timestamp())
    now = (int)(now.timestamp())
    return finnhub_client.stock_candles(stock,resolution,prev,now)
