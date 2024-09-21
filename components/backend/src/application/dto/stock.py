from pydantic import BaseModel, Field

class Stock(BaseModel):
    ticker: str = Field()
    name: str = Field()

class StockPrice(BaseModel):
    ticker: str = Field()
    name: str = Field()