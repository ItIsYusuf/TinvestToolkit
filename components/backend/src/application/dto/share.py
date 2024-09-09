from attr import dataclass
from fastapi import Query
from pydantic import BaseModel, Field

@dataclass
class PaginationCommon:
    page: int = Query(ge=0, default=0)
    size: int = Query(ge=0, default=50, le=100)

class IDCommon(BaseModel):
    id: int = Field(
        description='PK',
        gt=0
    )