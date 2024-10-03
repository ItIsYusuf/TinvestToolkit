from attr import dataclass
from typing import List
from src.application import dto, interfaces
from src.adapters.external.tinkoff.tinkoff_api import TinkoffAPI
from src.adapters.cache.redis_client import get_redis_client

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
        redis = await get_redis_client()

        cached_stock = await redis.get(f"stock:{stock_id}")
        if cached_stock:
            return dto.Stock.parse_raw(cached_stock)

        stock = await self.client_stocks_repo.get_stock_by_ticker_async(stock_id)
        await redis.set(f"stock:{stock_id}", stock.json(), ex=3600)

        return stock

    async def check_stocks_prices(self):
        client_stocks: List[ClientStock] = await self.client_stocks_repo.get_all_client_stocks_async()

        for client_stock in client_stocks:
            token = await self.client_stocks_repo.get_token_by_client_id(client_stock.client_id)
            tinkoff_api = TinkoffAPI(token)
            stock_dto: dto.Stock = await self.client_stocks_repo.get_stock_by_ticker_async(client_stock.stock_id)
            stock_with_price = tinkoff_api.add_price_to_stock(stock_dto)

            if stock_with_price.price >= client_stock.sell_price:
                try:
                    order_id = tinkoff_api.sell_stocks(stock_with_price)
                    print(f"Sold stock {stock_with_price.ticker}. Order ID: {order_id}")
                except Exception as e:
                    print(f"Failed to sell stock {stock_with_price.ticker}: {str(e)}")