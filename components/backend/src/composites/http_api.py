from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from libs.security import jwt_strategy

from src.adapters import database, http_api, log
from src.adapters.database import repositories
from src.adapters.http_api import create_app
from src.adapters.http_api.dependencies import Services
from src.application import services

class Settings:
    http_api = http_api.Settings()
    db = database.Settings()

class Logger:
    log.configure(Settings.http_api.LOGGING_CONFIG, Settings.db.LOGGING_CONFIG)

class DB:
    engine = create_async_engine(Settings.db.DATABASE_URL, echo=Settings.db.DATABASE_DEBUG)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    security_repo = repositories.SecurityRepository(async_session_maker=async_session_maker)

class Application:
    security_service = services.SecurityService(security_repo=DB.security_repo)

def initial_security():
    jwt_strategy.set_secret_key(Settings.http_api.APP_SECRET_KEY)
    jwt_strategy.set_access_token_expires_minutes(Settings.http_api.APP_TOKEN_EXPIRE_MINUTES)

def initial_services():
    Services.security = Application.security_service

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