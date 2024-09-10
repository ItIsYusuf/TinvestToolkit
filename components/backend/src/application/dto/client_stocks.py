from datetime import datetime
from pydantic import BaseModel, Field


class ClientStock(BaseModel):
    client_id: int | None = Field()
    stock_id: int | None = Field()
    sell_price: float = Field()
    buy_price: float = Field()
    created_at: datetime = Field()