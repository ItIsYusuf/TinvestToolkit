from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from libs.security import jwt_strategy

from src.adapters import database, http_api, log
from src.adapters.database import repositories
from src.adapters.external.tinkoff.tinkoff_api import TinkoffAPI
from src.adapters.http_api import create_app
from src.adapters.http_api.dependencies import Services
from src.application import services
from src.adapters.email_sender.sender import NotificationMailSender
from src.adapters.email_sender.settings import Settings as EmailSettings

class Settings:
    http_api = http_api.Settings()
    db = database.Settings()
    email = EmailSettings()


class Logger:
    log.configure(Settings.http_api.LOGGING_CONFIG, Settings.db.LOGGING_CONFIG)


class DB:
    engine = create_async_engine(Settings.db.DATABASE_URL, echo=Settings.db.DATABASE_DEBUG)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    security_repo = repositories.SecurityRepository(async_session_maker=async_session_maker)
    client_stocks_repo = repositories.ClientStocksRepository(async_session_maker=async_session_maker)
    upd_stocks_repo = repositories.UpdStockRepository(async_session_maker=async_session_maker)


class ExternalAPIs:
    tinkoff_api = TinkoffAPI(token="")


class EmailSender:
    notification_sender = NotificationMailSender(
        smtp_sender=Settings.email.SMTP_SENDER,
        smtp_password=Settings.email.SMTP_PASSWORD,
        smtp_host=Settings.email.SMTP_HOST,
        smtp_port=Settings.email.SMTP_PORT
    )


class Application:
    security_service = services.SecurityService(security_repo=DB.security_repo)
    client_stocks_service = services.ClientStocksService(
        client_stocks_repo=DB.client_stocks_repo,
        tinkoff_api=ExternalAPIs.tinkoff_api,
        notification_sender=EmailSender.notification_sender
    )
    stock_service = services.StockService(
        security_repo=DB.security_repo,
        stock_api=ExternalAPIs.tinkoff_api
    )


def initial_security():
    jwt_strategy.set_secret_key(Settings.http_api.APP_SECRET_KEY)
    jwt_strategy.set_access_token_expires_minutes(Settings.http_api.APP_TOKEN_EXPIRE_MINUTES)


def initial_services():
    Services.security = Application.security_service
    Services.client_stocks = Application.client_stocks_service
    Services.stock_service = Application.stock_service


def initial_app():
    initial_security()
    initial_services()


initial_app()
app = create_app(
    is_debug=Settings.http_api.APP_IS_DEBUG,
    version=Settings.http_api.APP_VERSION,
    swagger_on=Settings.http_api.APP_SWAGGER_ON,
    title=Settings.http_api.APP_TITLE
)