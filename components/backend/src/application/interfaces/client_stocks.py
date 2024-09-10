from abc import ABC, abstractmethod
from src.application import dto, entities

class IClientStocksRepo(ABC):

    @abstractmethod
    async def add_stock_async(self, client_stock: dto.ClientStock) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_stock_async(self, client_stock: dto.ClientStock) -> bool:
        raise NotImplementedError
