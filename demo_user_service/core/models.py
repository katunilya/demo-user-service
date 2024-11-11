from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    PlainSerializer,
    SecretStr,
)

from .validators import has_numbers, has_special_symbols, longer_than


class Role(StrEnum):
    TL = "tl"
    SDE = "sde"
    SRE = "sre"
    QA = "qa"


type PasswordSecretStr = Annotated[
    SecretStr,
    BeforeValidator(longer_than(12)),
    BeforeValidator(has_numbers(3)),
    BeforeValidator(has_special_symbols),
    PlainSerializer(lambda f: f.get_secret_value(), when_used="json"),
]

type UUIDSerializable = Annotated[UUID, PlainSerializer(str, when_used="json")]


class UserInfo(BaseModel):
    first_name: str
    second_name: str


class UserIdentity(BaseModel):
    username: str
    password: SecretStr


class UserEntity(BaseModel):
    id: UUIDSerializable
    info: UserInfo
    identity: UserIdentity
    teams: Annotated[dict[UUIDSerializable, Role], Field(default_factory=dict)]


class TeamInfo(BaseModel):
    title: str
    description: str | None = None


class TeamEntity(BaseModel):
    id: UUIDSerializable
    info: TeamInfo
    members: Annotated[dict[UUIDSerializable, Role], Field(default_factory=dict)]
