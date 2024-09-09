from attr import dataclass
from sqlalchemy import exists, insert, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.application import dto, entities
from src.application.interfaces import ISecurityRepo

@dataclass
class SecurityRepository(ISecurityRepo):
    async_session_maker: async_sessionmaker

    async def email_exists(self, email: str) -> bool:
        exists_criteria = exists().where(entities.Client.email == email)
        query = select(entities.Client).where(exists_criteria)

        async with self.async_session_maker() as session:
            _res = await session.execute(query)

        return True if _res.scalar() else False

    async def register_async(self, user: dto.UserRegister) -> None:
        query = insert(entities.Client).values(user.model_dump())

        async with self.async_session_maker() as session:
            await session.execute(query)
            await session.commit()

        return None

    async def get_user(self, email: str) -> entities.Client | None:
        query = select(entities.Client).where(entities.Client.email == email)

        async with self.async_session_maker() as session:
            _res = await session.execute(query)

        return _res.scalar()