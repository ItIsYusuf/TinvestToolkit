from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from libs.scheduler import AsyncTask, Scheduler
from libs.scheduler import Settings as SchedulerSettings

from src.adapters import database, log
from src.adapters.database import repositories
from src.application import services
from src.adapters.external.tinkoff.tinkoff_api import TinkoffAPI
import time
import threading


class Settings:
    scheduler = SchedulerSettings()
    db = database.Settings()


class DB:
    engine = create_async_engine(Settings.db.DATABASE_URL, echo=Settings.db.DATABASE_DEBUG)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    upd_stock_repo = repositories.UpdStockRepository(async_session_maker=async_session_maker)
    security_repo = repositories.SecurityRepository(async_session_maker=async_session_maker)
    client_stocks_repo = repositories.ClientStocksRepository(async_session_maker=async_session_maker)


class ExternalAPIs:
    tinkoff_api = TinkoffAPI(token="")


class Application:
    upd_stock_service = services.UpdStockService(
        security_repo=DB.security_repo,
        stock_api=ExternalAPIs.tinkoff_api,
        upd_stock_repo=DB.upd_stock_repo
    )
    client_stocks_service = services.ClientStocksService(
        client_stocks_repo=DB.client_stocks_repo,
        tinkoff_api=ExternalAPIs.tinkoff_api
    )


class Logger:
    log.configure(Settings.scheduler.LOGGING_CONFIG)


class Tasks:
    tasks = [
        AsyncTask(
            name='upd_stocks',
            cron='0 0 * * *',
            job=lambda: Application.upd_stock_service.get_stocks(client_id=8)
        ),
        AsyncTask(
            name='check_prices',
            cron='*/1 * * * *',
            job=lambda: Application.client_stocks_service.check_stocks_prices()
        )
    ]

if __name__ == '__main__':
    Logger()
    scheduler = Scheduler(async_tasks=Tasks.tasks)
    scheduler.run()