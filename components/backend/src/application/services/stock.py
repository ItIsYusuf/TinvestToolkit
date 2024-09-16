from attr import dataclass
from typing import List
from src.application.interfaces import ISecurityRepo, IStockApi
from src.application.dto import Stock

@dataclass
class StockService:
    security_repo: ISecurityRepo
    stock_api: IStockApi

    async def get_available_stocks(self, client_id: int) -> List[Stock]:
        token = await self.security_repo.get_user_token(client_id)
        if not token:
            raise Exception("User token not found")

        self.stock_api.token = token
        stocks = self.stock_api.get_available_stocks()
        return stocks