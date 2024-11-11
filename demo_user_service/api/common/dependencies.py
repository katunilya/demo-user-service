from __future__ import annotations

from typing import Annotated, AsyncGenerator, cast
from uuid import UUID

from edgedb import AsyncIOClient
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from demo_user_service.core import NotFoundObjectError, PersistentStore, UserEntity
from demo_user_service.service import (
    AuthService,
    CacheService,
    EdgeDBPersistentStore,
    PersistentStoreCache,
)

from .lifespan import AppState

inject_jwt_token = OAuth2PasswordBearer(tokenUrl="/users/auth")


def inject_cache_service(request: Request) -> CacheService:
    return cast(AppState, request.state).cache_service


def inject_auth_service(request: Request) -> AuthService:
    return cast(AppState, request.state).auth_service


def inject_edgedb_client(request: Request) -> AsyncIOClient:
    return cast(AppState, request.state).edgedb_client


def inject_persistent_store(
    edgedb_client: EdgeDBClientDep,
    cache: CacheServiceDep,
) -> PersistentStore:
    return PersistentStoreCache(
        store=EdgeDBPersistentStore(edgedb_client),
        cache=cache,
    )


async def inject_tx_persistent_store(
    edgedb_client: EdgeDBClientDep,
    cache: CacheServiceDep,
) -> AsyncGenerator[PersistentStore]:
    async for tx in edgedb_client.transaction():
        async with tx:
            yield PersistentStoreCache(
                store=EdgeDBPersistentStore(executor=tx),
                cache=cache,
            )


def inject_request_author_id(
    token: AuthTokenDep,
    auth: AuthServiceDep,
) -> UUID:
    return auth.decode_user_id_from_token(token)


async def inject_request_author(
    author_id: RequestAuthorIdDep,
    store: PersistentStoreDep,
) -> UserEntity:
    entity = await store.select_user_by_id(user_id=author_id)

    if not entity:
        raise NotFoundObjectError(f"user [{author_id}]")

    return entity


# dependencies aliases
AuthTokenDep = Annotated[str, Depends(inject_jwt_token)]
AuthFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
RequestAuthorIdDep = Annotated[UUID, Depends(inject_request_author_id)]
RequestAuthorDep = Annotated[UserEntity, Depends(inject_request_author)]
AuthServiceDep = Annotated[AuthService, Depends(inject_auth_service)]
CacheServiceDep = Annotated[CacheService, Depends(inject_cache_service)]
EdgeDBClientDep = Annotated[AsyncIOClient, Depends(inject_edgedb_client)]
PersistentStoreDep = Annotated[PersistentStore, Depends(inject_persistent_store)]
TxPersistentStoreDep = Annotated[PersistentStore, Depends(inject_tx_persistent_store)]
