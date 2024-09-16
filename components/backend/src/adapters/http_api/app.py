from fastapi import FastAPI

from src.adapters.http_api import controllers
def create_app(
        version: str,
        is_debug: bool = False,
        swagger_on: bool = False,
        title: str = 'TinvestToolkit'
) -> FastAPI:
    app = FastAPI(
        title=title,
        debug=is_debug,
        version=version,
        docs_url='/docs' if swagger_on else None,
        redoc_url='/redoc' if swagger_on else None,
    )
    app.include_router(controllers.security_router)
    app.include_router(controllers.stock_router)
    app.include_router(controllers.client_stocks)
    return app