from attr import dataclass
from typing import List
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application.interfaces import IUpdStockRepo
from src.application import dto, entities
from src.application.entities import Stocks
from src.application.dto import Stock

@dataclass
class UpdStockRepository(IUpdStockRepo):
    async_session_maker: async_sessionmaker

    async def add_stocks_async(self, stocks: List[Stock]) -> None:

        async with self.async_session_maker() as session:
            for stock in stocks:
                query = select(Stocks).where(
                    Stocks.ticker == stock.ticker,
                    Stocks.company_name == stock.name
                )
                result = await session.execute(query)
                existing_stock = result.scalar_one_or_none()

                if not existing_stock:
                    query = insert(Stocks).values(
                        ticker=stock.ticker,
                        company_name=stock.name
                    )
                    await session.execute(query)

            await session.commit()

        return None