from pydantic import BaseModel, Field

class Stock(BaseModel):
    ticker: str = Field()
    name: str = Field()
    price: float | None = Field(default=None)

class StockPrice(BaseModel):
    ticker: str = Field()
    name: str = Field()