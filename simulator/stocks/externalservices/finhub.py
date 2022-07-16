import finnhub
import core.settings as settings;

def lookup_stocks(data):
    finnhub_client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)
    return (finnhub_client.symbol_lookup(data))
