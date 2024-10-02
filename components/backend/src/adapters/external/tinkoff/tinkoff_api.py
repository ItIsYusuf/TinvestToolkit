from tinkoff.invest import Client
from tinkoff.invest.schemas import Quotation, OrderDirection, OrderType
from tinkoff.invest.services import GetAccountsResponse
from src.application.dto import Stock, StockPrice, ClientStock
from typing import List
import uuid
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

    def get_active_account(self) -> str:
        with Client(self.token) as client:
            accounts = client.users.get_accounts()
            for account in accounts.accounts:
                print(f"Account ID: {account.id}, Type: {account.type}, Name: {account.name}, Status: {account.status}")
                if account.status == 2:
                    return account.id

            raise ValueError("No active accounts found")

    def sell_stocks(self, stock: Stock) -> str:
        with Client(self.token) as client:
            instruments = client.instruments.shares()
            figi = None
            for share in instruments.instruments:
                if share.ticker == stock.ticker:
                    figi = share.figi
                    break

            if not figi:
                raise ValueError(f"FIGI not found for ticker {stock.ticker}")

            account_id = self.get_active_account()

            order_id = str(uuid.uuid4())

            order = client.orders.post_order(
                figi=figi,
                quantity=1,
                direction=OrderDirection.ORDER_DIRECTION_SELL,
                account_id=account_id,
                order_type=OrderType.ORDER_TYPE_MARKET,
                order_id=order_id
            )

            return order.order_id