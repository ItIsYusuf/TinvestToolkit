from attr import dataclass
from typing import List
from src.application import dto, interfaces
from src.adapters.external.tinkoff.tinkoff_api import TinkoffAPI
@dataclass
class ClientStocksService:
    client_stocks_repo: interfaces.IClientStocksRepo
    tinkoff_api: TinkoffAPI

    async def add_stock_async(self, client_stock: dto.ClientStock):
        exists = await self.client_stocks_repo.check_stock_async(client_stock)
        if exists:
            raise ValueError("Already exists")

        await self.client_stocks_repo.add_stock_async(client_stock)

    async def get_stock_by_ticker_async(self, stock_id: int) -> dto.Stock:
        stock = await self.client_stocks_repo.get_stock_by_ticker_async(stock_id)
        return stock

    async def check_stocks_prices(self):
        client_stocks: List[ClientStock] = await self.client_stocks_repo.get_all_client_stocks_async()

        for client_stock in client_stocks:
            token = await self.client_stocks_repo.get_token_by_client_id(client_stock.client_id)
            tinkoff_api = TinkoffAPI(token)
            stock_dto: dto.Stock = await self.client_stocks_repo.get_stock_by_ticker_async(client_stock.stock_id)
            stock_with_price = tinkoff_api.add_price_to_stock(stock_dto)

            if stock_with_price.price >= client_stock.sell_price:
                print(f"It's time to sell this stock for client {client_stock.client_id}")