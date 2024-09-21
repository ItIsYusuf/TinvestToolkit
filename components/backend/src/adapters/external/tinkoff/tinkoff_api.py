from tinkoff.invest import Client
from src.application.dto import Stock, StockPrice
from typing import List

class TinkoffAPI:
    def __init__(self, token: str):
        self.token = token

    def get_available_stocks(self) -> List[Stock]:
        with Client(self.token) as client:
            response = client.instruments.shares()
            stocks = [
                Stock(ticker=share.ticker, name=share.name)
                for share in response.instruments if share.buy_available_flag
            ]
        return stocks

    def get_stocks(self) -> List[Stock]:
        with Client(self.token) as client:
            response = client.instruments.shares()
            stocks = [
                Stock(ticker=share.ticker, name=share.name)
                for share in response.instruments
            ]
        return stocks

    def get_stock_price(self, ticker: str) -> StockPrice:
        with Client(self.token) as client:
            response = client.instruments.find_instrument(query=ticker)
            if not response.instruments:
                raise ValueError(f"Stock with '{ticker}' not found")

            figi = response.instruments[0].figi

            market_data = client.market_data.get_last_prices(
                figi=[figi]
            )

            if not market_data.last_prices:
                raise ValueError(f"Price for stock with FIGI '{figi}' not found")

            last_price = market_data.last_prices[0].price
            return StockPrice(ticker=ticker, price=last_price.units + last_price.nano /1e9)