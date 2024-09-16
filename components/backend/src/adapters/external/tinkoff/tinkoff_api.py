from tinkoff.invest import Client
from src.application.dto import Stock
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