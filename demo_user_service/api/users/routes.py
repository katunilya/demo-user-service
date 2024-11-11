from uuid import UUID

from fastapi import APIRouter
from pydantic import SecretStr

from demo_user_service.api.common import (
    AuthFormDep,
    AuthServiceDep,
    FilterQuery,
    PersistentStoreDep,
    RequestAuthorDep,
    RequestAuthorIdDep,
)
from demo_user_service.core import (
    InvalidPasswordError,
    NotFoundObjectError,
    UserIdentity,
    UserInfo,
)

from .contracts import (
    AuthTokenResponse,
    UserRegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def post_users_register(
    body: UserRegisterRequest,
    auth: AuthServiceDep,
    store: PersistentStoreDep,
) -> UserResponse:
    hashed_password = auth.secure_password(body.password)

    entity = await store.insert_user(
        info=UserInfo(
            first_name=body.first_name,
            second_name=body.second_name,
        ),
        identity=UserIdentity(
            username=body.username,
            password=hashed_password,
        ),
    )

    return UserResponse.from_entity(entity)


@router.post("/auth")
async def post_users_auth(
    auth_form: AuthFormDep,
    store: PersistentStoreDep,
    auth: AuthServiceDep,
) -> AuthTokenResponse:
    entity = await store.select_user_by_username(username=auth_form.username)

    if not entity:
        raise NotFoundObjectError(f"user [{auth_form.username}]")

    if not auth.passwords_match(
        password=SecretStr(auth_form.password),
        hashed_password=entity.identity.password,
    ):
        raise InvalidPasswordError(f"user [{entity.id}]")

    token = auth.encode_token_for_user(user=entity)

    return AuthTokenResponse(access_token=token)


@router.get("/me")
async def get_users_me(author: RequestAuthorDep) -> UserResponse:
    return UserResponse.from_entity(author)


@router.get("/{user_id}")
async def get_users_by_id(
    user_id: UUID,
    store: PersistentStoreDep,
    _: RequestAuthorIdDep,
) -> UserResponse:
    entity = await store.select_user_by_id(user_id=user_id)

    if not entity:
        raise NotFoundObjectError(message=f"user [{user_id}]")

    return UserResponse.from_entity(entity)


@router.get("")
async def get_users(
    filter: FilterQuery,
    store: PersistentStoreDep,
    _: RequestAuthorIdDep,
) -> list[UserResponse]:
    entities = await store.select_users(
        offset=filter.offset,
        limit=filter.limit,
    )

    return [UserResponse.from_entity(entity) for entity in entities]


@router.delete(
    "/{user_id}",
)
async def delete_users_by_id(
    user_id: UUID,
    store: PersistentStoreDep,
    _: RequestAuthorIdDep,
):
    await store.delete_user(user_id=user_id)
