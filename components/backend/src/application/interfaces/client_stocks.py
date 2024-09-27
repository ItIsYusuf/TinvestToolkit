from abc import ABC, abstractmethod
from typing import List
from src.application import dto, entities

class IClientStocksRepo(ABC):

    @abstractmethod
    async def add_stock_async(self, client_stock: dto.ClientStock) -> None:
        raise NotImplementedError

    @abstractmethod
    async def check_stock_async(self, client_stock: dto.ClientStock) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_stock_by_ticker_async(self, stock_id: int) -> dto.Stock:
        raise NotImplementedError

    @abstractmethod
    async def get_all_client_stocks_async(self) -> List[dto.Stock]:
        raise NotImplementedError