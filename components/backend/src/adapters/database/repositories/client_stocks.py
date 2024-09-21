from attr import dataclass
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application import dto, entities
from src.application.interfaces import IClientStocksRepo

@dataclass
class ClientStocksRepository(IClientStocksRepo):
    async_session_maker: async_sessionmaker

    async def check_stock_async(self, client_stock: dto.ClientStock) -> bool:
        query = select(entities.ClientStocks.client_id).where(
            entities.ClientStocks.client_id == client_stock.client_id,
            entities.ClientStocks.stock_id == client_stock.stock_id
        )

        async with self.async_session_maker() as session:
            _res = await session.execute(query)

        return True if _res.scalar() else False

    async def add_stock_async(self, client_stock: dto.ClientStock) -> None:
        query = insert(entities.ClientStocks).values(client_stock.model_dump())

        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()
