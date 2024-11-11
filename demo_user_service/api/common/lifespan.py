from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Protocol, TypedDict

from edgedb import AsyncIOClient, create_async_client
from fastapi import FastAPI

from demo_user_service.core.models import UserIdentity, UserInfo
from demo_user_service.service import (
    AuthConfig,
    AuthService,
    CacheConfig,
    CacheService,
    EdgeDBConfig,
)
from demo_user_service.service.edgedb import EdgeDBPersistentStore

from .config import APIConfig


class _AppState(TypedDict):
    auth_service: AuthService
    cache_service: CacheService
    edgedb_client: AsyncIOClient


class AppState(Protocol):
    auth_service: AuthService
    cache_service: CacheService
    edgedb_client: AsyncIOClient


@asynccontextmanager
async def startup_and_shutdown(_: FastAPI):
    edgedb_config = EdgeDBConfig()
    api_config = APIConfig()

    auth_service = AuthService(config=AuthConfig())

    async with (
        CacheService(config=CacheConfig()) as cache_service,
        create_async_client(
            dsn=edgedb_config.DSN,
            tls_security=edgedb_config.TLS_SECURITY,
        ) as edgedb_client,
    ):
        store = EdgeDBPersistentStore(edgedb_client)
        await _initialize_admin(store, auth_service, api_config)

        yield _AppState(
            auth_service=auth_service,
            cache_service=cache_service,
            edgedb_client=edgedb_client,
        )


async def _initialize_admin(
    store: EdgeDBPersistentStore,
    auth_service: AuthService,
    config: APIConfig,
) -> None:
    admin = await store.select_user_by_username(username="admin")

    if admin:
        return

    password = auth_service.secure_password(config.ADMIN_PASSWORD)
    await store.insert_user(
        info=UserInfo(first_name="", second_name=""),
        identity=UserIdentity(
            username=config.ADMIN_USERNAME,
            password=password.get_secret_value(),
        ),
    )
