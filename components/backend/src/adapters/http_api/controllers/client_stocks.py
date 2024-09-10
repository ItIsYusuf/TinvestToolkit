from typing import Annotated
from fastapi import APIRouter, Body, Depends
from src.adapters.http_api.auth import verify_jwt
from src.adapters.http_api.dependencies import client_stocks_service
from src.application import dto
from src.application.services import ClientStocksService

router = APIRouter(
    prefix='/client-stocks',
    tags=['Client\'s stocks']
)

@router.post('/add-stock')
async def add_stock_async(
        client_stocks_service: Annotated[ClientStocksService, Depends(client_stocks_service)],
        token: str = Depends(verify_jwt),
        client_stock: dto.ClientStock = Body()
):
    await client_stocks_service.add_stock_async(client_stock)
    return {"message": "Stock added successfully"}
