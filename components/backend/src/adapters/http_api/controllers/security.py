from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response

from libs.security import jwt_strategy

from src.adapters.http_api.dependencies import security_service
from src.application import dto
from src.application.services import SecurityService

router = APIRouter(
    prefix='/security',
    tags=['Authorization']
)


@router.post(path='/login')
async def login_for_access_token(
        security_service: Annotated[SecurityService, Depends(security_service)],
        response: Response,
        user: dto.UserLogin = Body(),
):
    await security_service.login_async(user)
    token = jwt_strategy.create_access_token()
    response.set_cookie(key='token', value=token)


@router.post(path='/register')
async def register_for_access_token(
        security_service: Annotated[SecurityService, Depends(security_service)],
        response: Response,
        user: dto.UserRegister = Body()
):
    await security_service.register_async(user)
    token = jwt_strategy.create_access_token()
    response.set_cookie(key='token', value=token)