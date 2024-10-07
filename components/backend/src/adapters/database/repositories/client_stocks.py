from attr import dataclass
from typing import List, Optional
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.application import dto, entities
from src.application.interfaces import IClientStocksRepo
from datetime import timezone

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
        client_stock.created_at = client_stock.created_at.replace(tzinfo=None)
        query = insert(entities.ClientStocks).values(client_stock.model_dump())

        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()


    async def get_stock_by_ticker_async(self, stock_id: int) -> dto.Stock:
        query = select(entities.Stocks).where(entities.Stocks.id == stock_id)

        async with self.async_session_maker() as session:
            _res = await session.execute(query)
            stock_entity = _res.scalar_one_or_none()
            stock_dto = dto.Stock(ticker=stock_entity.ticker, name=stock_entity.company_name)
            return stock_dto


    async def get_all_client_stocks_async(self) -> List[dto.ClientStock]:
        query = select(entities.ClientStocks)

        async with self.async_session_maker() as session:
            result = await session.execute(query)
            return result.scalars().all()


    async def get_token_by_client_id(self, client_id: int) -> str:
        query = select(entities.Client.token).where(entities.Client.id == client_id)

        async with self.async_session_maker() as session:
            _res = await session.execute(query)
            token = _res.scalar_one_or_none()
            if not token:
                raise ValueError("Token not found")
            return token

    async def get_email_by_client_id(self, client_id: int) -> Optional[str]:
        query = select(entities.Client.email).where(entities.Client.id == client_id)
        async with self.async_session_maker() as session:
            _res = await session.execute(query)
            email = _res.scalar_one_or_none()
            return email