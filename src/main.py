from fastapi                   import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routes            import (
	category_router,
	order_router,
	product_router,
	subcategory_router
)
from src.config                import app_configs, settings

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins      = settings.CORS_ORIGINS,
    allow_origin_regex = settings.CORS_ORIGINS_REGEX,
    allow_credentials  = True,
    allow_methods      = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    allow_headers      = settings.CORS_HEADERS,
)

app.include_router(category_router,    prefix='/category',    tags=['category'])
app.include_router(order_router,       prefix='/order',       tags=['order'])
app.include_router(product_router,     prefix='/product',     tags=['product'])
app.include_router(subcategory_router, prefix='/subcategory', tags=['subcategory'])
