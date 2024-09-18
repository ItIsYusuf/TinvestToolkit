from attr import dataclass
from typing import List
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application.interfaces import IUpdStockRepo
from src.application import dto, entities
from src.application.entities import Stocks
from src.application.dto import Stock

@dataclass
class UpdStockRepository(IUpdStockRepo):
    async_session_maker: async_sessionmaker

    async def add_stocks_async(self, stocks: List[Stock]) -> None:
        stock_data = [{'ticker': stock.ticker, 'company_name': stock.name} for stock in stocks]
        query = insert(Stocks).values(stock_data)

        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()

        return None