from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from .log import logging
from .routes import index, auth


allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://4ad3-119-82-92-120.ngrok-free.app"
]
allowed_methods = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS"
]
allowed_headers = {
    "*"
}

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
    max_age=3600
)

app.include_router(index.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")