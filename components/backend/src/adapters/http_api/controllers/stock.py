from typing import Annotated
from fastapi import APIRouter, Depends
from src.adapters.http_api.auth import verify_jwt
from src.adapters.http_api.dependencies import stock_service
from src.application.dto import Stock
from src.application.services import StockService

router = APIRouter(
    prefix='/stocks',
    tags=['Stocks']
)


@router.get('/available')
async def get_available_stocks(
        stock_service: Annotated[StockService, Depends(stock_service)],
        token: dict = Depends(verify_jwt)
):
    client_id = token.get('client_id')
    if client_id is None:
        raise
    stocks = await stock_service.get_available_stocks(client_id)

    return [Stock(ticker=stock.ticker, name=stock.name) for stock in stocks]
