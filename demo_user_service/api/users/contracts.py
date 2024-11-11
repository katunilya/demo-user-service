from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from demo_user_service.api.common import CamelCaseContract
from demo_user_service.core import PasswordSecretStr, Role, UserEntity


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserRegisterRequest(CamelCaseContract):
    username: str
    first_name: str
    second_name: str
    password: PasswordSecretStr


class UserResponse(CamelCaseContract):
    id: UUID
    username: str
    first_name: str
    second_name: str
    teams: dict[UUID, Role]

    @staticmethod
    def from_entity(entity: UserEntity) -> UserResponse:
        return UserResponse(
            id=entity.id,
            username=entity.identity.username,
            first_name=entity.info.first_name,
            second_name=entity.info.second_name,
            teams=entity.teams,
        )
