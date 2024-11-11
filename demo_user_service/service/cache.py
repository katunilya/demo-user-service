from dataclasses import dataclass, field
from types import TracebackType
from typing import Self

from pydantic_settings import BaseSettings
from redis.asyncio.client import Redis


class CacheConfig(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_USER: str | None = None
    REDIS_DB: int = 0

    PREFIX: str = "dus"
    DEFAULT_TTL_SECONDS: int | None = None

    ENABLED: bool = True

    model_config = {
        "env_prefix": "CACHE_",
    }


@dataclass(slots=True)
class CacheService:
    config: CacheConfig

    _redis_client: Redis = field(init=False)

    def __post_init__(self) -> None:
        self._redis_client = Redis(
            host=self.config.REDIS_HOST,
            port=self.config.REDIS_PORT,
            db=self.config.REDIS_DB,
            password=self.config.REDIS_PASSWORD,
        )

    async def __aenter__(self) -> Self:
        self._redis_client = await self._redis_client.initialize()
        return self

    async def __aexit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        await self._redis_client.close()

    async def save(
        self,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        if not self.config.ENABLED:
            return

        await self._redis_client.set(
            name=f"{self.config.PREFIX}/{key}",
            value=value,
            ex=ttl_seconds or self.config.DEFAULT_TTL_SECONDS,
        )

    async def get(
        self,
        key: str,
    ) -> str | None:
        if not self.config.ENABLED:
            return None

        response: bytes | None = await self._redis_client.get(
            name=f"{self.config.PREFIX}/{key}"
        )

        if response:
            return response.decode("utf-8")

        return None

    async def delete(
        self,
        key: str,
    ) -> None:
        if not self.config.ENABLED:
            return None

        await self._redis_client.delete(f"{self.config.PREFIX}/{key}")
