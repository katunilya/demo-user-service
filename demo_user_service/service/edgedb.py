from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from edgedb import AsyncIOExecutor
from pydantic_settings import BaseSettings

from demo_user_service.core import (
    Role,
    TeamEntity,
    TeamInfo,
    UserEntity,
    UserIdentity,
    UserInfo,
)
from demo_user_service.core.protocols import PersistentStore

from .queries import (
    UserRole02,
    delete_user,
    insert_team,
    insert_user,
    select_team_by_id,
    select_teams,
    select_user_by_id,
    select_user_by_login,
    select_users,
    update_user_add_team_link,
    update_user_remove_team_link,
    update_user_team_link,
)


class EdgeDBConfig(BaseSettings):
    DSN: str = "edgedb://edgedb:edgedbPassword@localhost:5656/main"
    TLS_SECURITY: str = "insecure"

    model_config = {
        "env_prefix": "EDGEDB_STORE_",
    }


@dataclass(slots=True)
class EdgeDBPersistentStore(PersistentStore):
    executor: AsyncIOExecutor

    async def insert_user(
        self,
        info: UserInfo,
        identity: UserIdentity,
    ) -> UserEntity:
        user = await insert_user(
            self.executor,
            login=identity.username,
            first_name=info.first_name,
            second_name=info.second_name,
            password=identity.password.get_secret_value(),
        )

        return UserEntity(
            id=user.id,
            info=info,
            identity=identity,
        )

    async def add_user_to_team(
        self,
        user_id: UUID,
        team_id: UUID,
        role: Role,
    ) -> None:
        await update_user_add_team_link(
            self.executor,
            user_id=user_id,
            team_id=team_id,
            role=UserRole02(role.value.upper()),
        )

    async def remove_user_from_team(
        self,
        user_id: UUID,
        team_id: UUID,
    ) -> None:
        await update_user_remove_team_link(
            self.executor,
            user_id=user_id,
            team_id=team_id,
        )

    async def update_user_role_in_team(
        self,
        user_id: UUID,
        team_id: UUID,
        role: Role,
    ) -> None:
        await update_user_team_link(
            self.executor,
            user_id=user_id,
            team_id=team_id,
            role=UserRole02(role.value.upper()),
        )

    async def select_user_by_username(
        self,
        username: str,
    ) -> UserEntity | None:
        result = await select_user_by_login(self.executor, login=username)

        if not result:
            return result

        return UserEntity(
            id=result.id,
            info=UserInfo(
                first_name=result.first_name,
                second_name=result.second_name,
            ),
            identity=UserIdentity(
                username=result.login,
                password=result.password,
            ),
            teams={t.id: Role(t["@role"].value.lower()) for t in result.teams},
        )

    async def select_user_by_id(
        self,
        user_id: UUID,
    ) -> UserEntity | None:
        result = await select_user_by_id(self.executor, user_id=user_id)

        if not result:
            return result

        return UserEntity(
            id=result.id,
            info=UserInfo(
                first_name=result.first_name,
                second_name=result.second_name,
            ),
            identity=UserIdentity(
                username=result.login,
                password=result.password,
            ),
            teams={t.id: Role(t["@role"].value.lower()) for t in result.teams},
        )

    async def select_users(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[UserEntity]:
        results = await select_users(self.executor, offset=offset, limit=limit)

        return [
            UserEntity(
                id=result.id,
                info=UserInfo(
                    first_name=result.first_name,
                    second_name=result.second_name,
                ),
                identity=UserIdentity(
                    username=result.login,
                    password=result.password,
                ),
                teams={t.id: Role(t["@role"].value.lower()) for t in result.teams},
            )
            for result in results
        ]

    async def delete_user(
        self,
        user_id: str,
    ) -> None:
        await delete_user(self.executor, user_id=user_id)

    async def insert_team(
        self,
        info: TeamInfo,
        tl_id: UUID,
    ) -> TeamEntity:
        result = await insert_team(
            self.executor,
            user_id=tl_id,
            title=info.title,
            description=info.description,
        )

        return TeamEntity(
            id=result.teams[0].id,
            info=info,
            members={tl_id: Role.TL},
        )

    async def select_team_by_id(
        self,
        team_id: UUID,
    ) -> TeamEntity | None:
        result = await select_team_by_id(self.executor, team_id=team_id)

        if not result:
            return None

        return TeamEntity(
            id=result.id,
            info=TeamInfo(
                title=result.title,
                description=result.description,
            ),
            members={m.id: Role(m["@role"].value.lower()) for m in result.members},
        )

    async def select_teams(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[TeamEntity]:
        results = await select_teams(self.executor, offset=offset, limit=limit)

        return [
            TeamEntity(
                id=result.id,
                info=TeamInfo(
                    title=result.title,
                    description=result.description,
                ),
                members={m.id: Role(m["@role"].value.lower()) for m in result.members},
            )
            for result in results
        ]
