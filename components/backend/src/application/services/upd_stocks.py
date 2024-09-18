from attr import dataclass
from typing import List
from src.application.interfaces import ISecurityRepo, IUpdStockRepo
from src.application.dto import Stock

@dataclass
class UpdStockService:
    security_repo: ISecurityRepo
    stock_api: IUpdStockRepo
    upd_stock_repo: IUpdStockRepo
    async def get_stocks(self, client_id: int) -> List[Stock]:
        token = await self.security_repo.get_user_token(client_id)
        if not token:
            raise Exception("User token not found")

        self.stock_api.token = token
        stocks = self.stock_api.get_stocks()
        await self.upd_stock_repo.add_stocks_async(stocks)
        return stocks