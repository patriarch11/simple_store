from contextlib                import asynccontextmanager

from fastapi                   import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config                import app_configs, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup database

    yield

app = FastAPI(
    **app_configs,
    lifespan = lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins      = settings.CORS_ORIGINS,
    allow_origin_regex = settings.CORS_ORIGINS_REGEX,
    allow_credentials  = True,
    allow_methods      = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    allow_headers      = settings.CORS_HEADERS,
)
