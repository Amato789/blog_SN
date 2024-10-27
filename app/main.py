from fastapi import FastAPI
from app.users.router import router as router_users
from app.posts.router import router as router_posts
from app.analytics.router import router as router_analytics
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from redis import asyncio as aioredis
from app.config import settings
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title='Blog StarNavi',
    root_path="/api",
    description='Blog StarNavi',
    debug=True,
    lifespan=lifespan,
)


app.include_router(router_users)
app.include_router(router_posts)
app.include_router(router_analytics)
