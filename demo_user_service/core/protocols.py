from typing import Protocol
from uuid import UUID

from .models import Role, TeamEntity, TeamInfo, UserEntity, UserIdentity, UserInfo


class PersistentStore(Protocol):
    async def insert_user(
        self,
        info: UserInfo,
        identity: UserIdentity,
    ) -> UserEntity: ...

    async def add_user_to_team(
        self,
        user_id: UUID,
        team_id: UUID,
        role: Role,
    ) -> None: ...

    async def remove_user_from_team(
        self,
        user_id: UUID,
        team_id: UUID,
    ) -> None: ...

    async def update_user_role_in_team(
        self,
        user_id: UUID,
        team_id: UUID,
        role: Role,
    ) -> None: ...

    async def select_user_by_username(
        self,
        username: str,
    ) -> UserEntity | None: ...

    async def select_user_by_id(
        self,
        user_id: UUID,
    ) -> UserEntity | None: ...

    async def select_users(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[UserEntity]: ...

    async def delete_user(
        self,
        user_id: str,
    ) -> None: ...

    async def insert_team(
        self,
        info: TeamInfo,
        tl_id: UUID,
    ) -> TeamEntity: ...

    async def select_team_by_id(
        self,
        team_id: UUID,
    ) -> TeamEntity | None: ...

    async def select_teams(
        self,
        offset: int = 0,
        limit: int = 10,
    ) -> list[TeamEntity]: ...
