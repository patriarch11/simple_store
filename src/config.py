from typing                         import Any

from dotenv                         import load_dotenv
from pydantic                       import PostgresDsn
from pydantic_settings              import BaseSettings

from src.constants                  import Environment


class Config(BaseSettings):
	DEBUG              : bool        = False
	ENVIRONMENT        : Environment = Environment.PRODUCTION

	CORS_ORIGINS       : list[str]
	CORS_ORIGINS_REGEX : str | None  = None
	CORS_HEADERS       : list[str]

	DATABASE_URL       : PostgresDsn

load_dotenv()
settings = Config()

app_configs: dict[str, Any] = {
	'debug': settings.DEBUG,
}

if not settings.ENVIRONMENT.is_debug:
	app_configs['openapi_url'] = None  # hide docs
	