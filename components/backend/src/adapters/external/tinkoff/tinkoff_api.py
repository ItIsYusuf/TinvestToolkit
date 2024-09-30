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


    def add_price_to_stock(self, stock: Stock) -> Stock:
        with Client(self.token) as client:
            instruments = client.instruments.shares()
            figi = None
            for share in instruments.instruments:
                if share.ticker == stock.ticker:
                    figi = share.figi
                    break
            if not figi:
                raise ValueError("Stock not found")

            last_prices = client.market_data.get_last_prices(figi=[figi])
            if last_prices.last_prices:
                price = (last_prices.last_prices[0].price.units + last_prices.last_prices[0].price.nano / 1e9)
                print(price)
                stock.price = price
                return stock
            else:
                raise ValueError("Price not found")