from abc import ABC, abstractmethod
from typing import List
from src.application.dto import Stock

class IUpdStockRepo(ABC):
    @abstractmethod
    async def add_stocks_async(self, stocks: List[Stock]) -> None:
        raise NotImplementedError