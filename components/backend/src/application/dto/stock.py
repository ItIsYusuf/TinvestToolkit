from pydantic import BaseModel, Field

class Stock(BaseModel):
    ticker: str = Field()
    name: str = Field()