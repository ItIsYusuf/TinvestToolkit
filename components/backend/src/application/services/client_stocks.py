from attr import dataclass
from src.application import dto, interfaces

@dataclass
class ClientStocksService:
    client_stocks_repo: interfaces.IClientStocksRepo

    async def add_stock_async(self, client_stock: dto.ClientStock):
        exists = await self.client_stocks_repo.check_stock_async(client_stock)
        if exists:
            raise ValueError("Already exists")

        await self.client_stocks_repo.add_stock_async(client_stock)
