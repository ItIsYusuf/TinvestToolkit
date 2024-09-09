from abc import ABC, abstractmethod

from src.application import dto, entities

class ISecurityRepo(ABC):
    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def register_async(self, user: dto.UserRegister) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, email: str) -> entities.Client | None:
        raise NotImplementedError