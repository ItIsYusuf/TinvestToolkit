from fastapi import HTTPException, Request, status

from libs.security import jwt_strategy

async def verify_jwt(
        request: Request
) -> dict | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    decode_token = jwt_strategy.verify_token(request.cookies.get('token', ''))
    if decode_token is None:
        raise credentials_exception
    return decode_token