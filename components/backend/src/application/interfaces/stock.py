from abc import ABC, abstractmethod
from typing import List
from src.application.dto import Stock, StockPrice

class IStockApi(ABC):
    @abstractmethod
    def get_available_stocks(self) -> List[Stock]:
        raise NotImplementedError

    @abstractmethod
    async def get_stock_price(self, ticker: str) -> StockPrice:
        raise NotImplementedError