from fastapi                   import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.config                import app_configs, settings
from src.dependencies          import (
	get_category_router,
	get_order_router,
	get_product_router,
	get_subcategory_router
)

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins      = settings.CORS_ORIGINS,
    allow_origin_regex = settings.CORS_ORIGINS_REGEX,
    allow_credentials  = True,
    allow_methods      = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    allow_headers      = settings.CORS_HEADERS,
)

app.include_router(get_category_router(),    prefix='/category',    tags=['category'])
app.include_router(get_order_router(),       prefix='/order',       tags=['order'])
app.include_router(get_product_router(),     prefix='/product',     tags=['product'])
app.include_router(get_subcategory_router(), prefix='/subcategory', tags=['subcategory'])
