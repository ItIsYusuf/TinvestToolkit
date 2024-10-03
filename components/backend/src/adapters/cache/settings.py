from pydantic import Extra, AnyUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    REDIS_URL: AnyUrl

    @property
    def LOGGING_CONFIG(self):
        return {
            'loggers': {
                'gunicorn': {
                    'handlers': ['default'],
                    'level': self.APP_LOGGING_LEVEL,
                    'propagate': False
                },
                'uvicorn': {
                    'handlers': ['default'],
                    'level': self.APP_LOGGING_LEVEL,
                    'propagate': False
                },
            }
        }

    class Config:
        extra = Extra.ignore
        env_file = '.env'
        env_file_encoding = 'utf-8'