from abc import ABC, abstractmethod
from typing import List
from src.application.dto import Stock

class IStockApi(ABC):
    @abstractmethod
    def get_available_stocks(self) -> List[Stock]:
        raise NotImplementedError