# AUTOGENERATED FROM:
#     'demo_user_service/service/queries/delete_user.edgeql'
#     'demo_user_service/service/queries/insert_team.edgeql'
#     'demo_user_service/service/queries/insert_user.edgeql'
#     'demo_user_service/service/queries/select_team_by_id.edgeql'
#     'demo_user_service/service/queries/select_teams.edgeql'
#     'demo_user_service/service/queries/select_user_by_id.edgeql'
#     'demo_user_service/service/queries/select_user_by_login.edgeql'
#     'demo_user_service/service/queries/select_users.edgeql'
#     'demo_user_service/service/queries/update_user_add_team_link.edgeql'
#     'demo_user_service/service/queries/update_user_remove_team_link.edgeql'
#     'demo_user_service/service/queries/update_user_team_link.edgeql'
# WITH:
#     $ edgedb-py -I demo_user_service_docker --target async --dir ./demo_user_service/service/queries --file ./demo_user_service/service/queries/__init__.py


from __future__ import annotations
import dataclasses
import edgedb
import enum
import typing
import uuid


class NoPydanticValidation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # Pydantic 2.x
        from pydantic_core.core_schema import any_schema
        return any_schema()

    @classmethod
    def __get_validators__(cls):
        # Pydantic 1.x
        from pydantic.dataclasses import dataclass as pydantic_dataclass
        _ = pydantic_dataclass(cls)
        cls.__pydantic_model__.__get_validators__ = lambda: []
        return []


@dataclasses.dataclass
class DeleteUserResult(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class InsertTeamResult(NoPydanticValidation):
    id: uuid.UUID
    teams: list[InsertTeamResultTeamsItem]


@dataclasses.dataclass
class InsertTeamResultTeamsItem(NoPydanticValidation):
    id: uuid.UUID


@dataclasses.dataclass
class SelectTeamByIdResult(NoPydanticValidation):
    id: uuid.UUID
    title: str
    description: str | None
    members: list[SelectTeamByIdResultMembersItem]


@dataclasses.dataclass
class SelectTeamByIdResultMembersItem(NoPydanticValidation):
    id: uuid.UUID

    @typing.overload
    def __getitem__(self, key: typing.Literal["@role"]) -> UserRole | None:
        ...

    def __getitem__(self, key: str) -> typing.Any:
        raise NotImplementedError


@dataclasses.dataclass
class SelectUserByIdResult(NoPydanticValidation):
    id: uuid.UUID
    login: str
    first_name: str
    second_name: str
    password: str
    teams: list[SelectUserByIdResultTeamsItem]


@dataclasses.dataclass
class SelectUserByIdResultTeamsItem(NoPydanticValidation):
    id: uuid.UUID

    @typing.overload
    def __getitem__(self, key: typing.Literal["@role"]) -> UserRole | None:
        ...

    def __getitem__(self, key: str) -> typing.Any:
        raise NotImplementedError


class UserRole(enum.Enum):
    TL = "TL"
    SDE = "SDE"
    SRE = "SRE"
    QA = "QA"


class UserRole02(enum.Enum):
    TL = "TL"
    SDE = "SDE"
    SRE = "SRE"
    QA = "QA"


async def delete_user(
    executor: edgedb.AsyncIOExecutor,
    *,
    user_id: uuid.UUID,
) -> DeleteUserResult | None:
    return await executor.query_single(
        """\
        update User
        filter .id = <uuid>$user_id
        set { deleted := true };\
        """,
        user_id=user_id,
    )


async def insert_team(
    executor: edgedb.AsyncIOExecutor,
    *,
    title: str,
    description: str | None = None,
    user_id: uuid.UUID,
) -> InsertTeamResult | None:
    return await executor.query_single(
        """\
        select (update User 
        filter .id = <uuid>$user_id
        set {
            teams += (insert Team {
                title := <str>$title,
                description := <optional str>$description,
                @role := UserRole.TL
            })
        }) {teams: {id}};\
        """,
        title=title,
        description=description,
        user_id=user_id,
    )


async def insert_user(
    executor: edgedb.AsyncIOExecutor,
    *,
    login: str,
    first_name: str,
    second_name: str,
    password: str,
) -> DeleteUserResult:
    return await executor.query_single(
        """\
        insert User {
            login := <str>$login,
            first_name := <str>$first_name,
            second_name := <str>$second_name,
            password := <str>$password
        };\
        """,
        login=login,
        first_name=first_name,
        second_name=second_name,
        password=password,
    )


async def select_team_by_id(
    executor: edgedb.AsyncIOExecutor,
    *,
    team_id: uuid.UUID,
) -> SelectTeamByIdResult | None:
    return await executor.query_single(
        """\
        select Team {
            id,
            title,
            description,
            members: {id, @role}
        }
        filter .id = <uuid>$team_id limit 1;\
        """,
        team_id=team_id,
    )


async def select_teams(
    executor: edgedb.AsyncIOExecutor,
    *,
    offset: int,
    limit: int,
) -> list[SelectTeamByIdResult]:
    return await executor.query(
        """\
        select Team {
            id,
            title,
            description,
            members: {id, @role}
        }
        offset <int64>$offset 
        limit <int64>$limit;\
        """,
        offset=offset,
        limit=limit,
    )


async def select_user_by_id(
    executor: edgedb.AsyncIOExecutor,
    *,
    user_id: uuid.UUID,
) -> SelectUserByIdResult | None:
    return await executor.query_single(
        """\
        select User {
            id, 
            login,
            first_name,
            second_name,
            password,
            teams: {
                id,
                @role
            }

        } filter .deleted = false and .id = <uuid>$user_id limit 1;\
        """,
        user_id=user_id,
    )


async def select_user_by_login(
    executor: edgedb.AsyncIOExecutor,
    *,
    login: str,
) -> SelectUserByIdResult | None:
    return await executor.query_single(
        """\
        select User {
            id, 
            login,
            first_name,
            second_name,
            password,
            teams: {
                id,
                @role
            }

        } filter .deleted = false and .login = <str>$login limit 1;\
        """,
        login=login,
    )


async def select_users(
    executor: edgedb.AsyncIOExecutor,
    *,
    offset: int,
    limit: int,
) -> list[SelectUserByIdResult]:
    return await executor.query(
        """\
        select User {
            id, 
            login,
            first_name,
            second_name,
            password,
            teams: {
                id,
                @role
            }
        }
        filter .deleted = false
        offset <int64>$offset
        limit <int64>$limit;\
        """,
        offset=offset,
        limit=limit,
    )


async def update_user_add_team_link(
    executor: edgedb.AsyncIOExecutor,
    *,
    team_id: uuid.UUID,
    role: UserRole02,
    user_id: uuid.UUID,
) -> DeleteUserResult | None:
    return await executor.query_single(
        """\
        update User
        filter .id = <uuid>$user_id
        set {
            teams += (
                select detached Team {
                    @role := <UserRole>$role
                }
                filter .id = <uuid>$team_id
            )
        };\
        """,
        team_id=team_id,
        role=role,
        user_id=user_id,
    )


async def update_user_remove_team_link(
    executor: edgedb.AsyncIOExecutor,
    *,
    team_id: uuid.UUID,
    user_id: uuid.UUID,
) -> DeleteUserResult | None:
    return await executor.query_single(
        """\
        update User
        filter .id = <uuid>$user_id
        set {
            teams -= (
                select detached Team
                filter .id = <uuid>$team_id
            )
        };\
        """,
        team_id=team_id,
        user_id=user_id,
    )


async def update_user_team_link(
    executor: edgedb.AsyncIOExecutor,
    *,
    team_id: uuid.UUID,
    role: UserRole02,
    user_id: uuid.UUID,
) -> DeleteUserResult | None:
    return await executor.query_single(
        """\
        update User
        filter .id = <uuid>$user_id
        set {
            teams := (
                select .teams {
                    @role := <UserRole>$role
                }
                filter .id = <uuid>$team_id
            )
        };\
        """,
        team_id=team_id,
        role=role,
        user_id=user_id,
    )