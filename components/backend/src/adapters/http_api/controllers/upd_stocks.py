from typing import Annotated
from fastapi import APIRouter, Depends
from src.adapters.http_api.auth import verify_jwt
from src.adapters.http_api.dependencies import upd_stock_service
from src.application.dto import Stock
from src.application.services import UpdStockService

router = APIRouter(
    prefix='/admin',
    tags=['Update database']
)

@router.get('/upd-stocks')
async def get_stocks(
        upd_stock_service: Annotated[UpdStockService, Depends(upd_stock_service)],
        token: dict = Depends(verify_jwt)
):
    client_id = token.get('client_id')
    if client_id is None:
        raise
    stocks = await upd_stock_service.get_stocks(client_id)
    return [Stock(ticker=stock.ticker, name=stock.name) for stock in stocks]