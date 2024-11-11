import json
from dataclasses import dataclass
from uuid import UUID

from pydantic import ValidationError

from demo_user_service.core import PersistentStore
from demo_user_service.core.models import (
    Role,
    TeamEntity,
    TeamInfo,
    UserEntity,
    UserIdentity,
    UserInfo,
)

from .cache import CacheService


@dataclass(slots=True)
class PersistentStoreCache(PersistentStore):
    store: PersistentStore
    cache: CacheService

    async def insert_user(self, info: UserInfo, identity: UserIdentity) -> UserEntity:
        user = await self.store.insert_user(info, identity)
        return await self._cache_user(user)

    async def add_user_to_team(self, user_id: UUID, team_id: UUID, role: Role) -> None:
        await self.store.add_user_to_team(user_id, team_id, role)
        user = await self._get_cached_user(user_id=user_id)
        if user:
            await self._delete_cached_user(user)

    async def remove_user_from_team(self, user_id: UUID, team_id: UUID) -> None:
        await self.store.remove_user_from_team(user_id, team_id)
        user = await self._get_cached_user(user_id=user_id)
        if user:
            await self._delete_cached_user(user)

    async def update_user_role_in_team(
        self, user_id: UUID, team_id: UUID, role: Role
    ) -> None:
        await self.store.update_user_role_in_team(user_id, team_id, role)
        user = await self._get_cached_user(user_id=user_id)
        if user:
            await self._delete_cached_user(user)

    async def select_user_by_username(self, username: str) -> UserEntity | None:
        user = await self._get_cached_user(username=username)

        if user:
            return user

        user = await self.store.select_user_by_username(username)

        if not user:
            return None

        return await self._cache_user(user)

    async def select_user_by_id(self, user_id: UUID) -> UserEntity | None:
        user = await self._get_cached_user(user_id=user_id)

        if user:
            return user

        user = await self.store.select_user_by_id(user_id)

        if not user:
            return None

        return await self._cache_user(user)

    async def select_users(self, offset: int = 0, limit: int = 10) -> list[UserEntity]:
        return await self.store.select_users(offset, limit)

    async def delete_user(self, user_id: str) -> None:
        await self.store.delete_user(user_id)

        user = await self._get_cached_user(user_id=user_id)

        if user:
            await self._delete_cached_user(user)

    async def insert_team(self, info: TeamInfo, tl_id: UUID) -> TeamEntity:
        team = await self.store.insert_team(info, tl_id)

        user = await self._get_cached_user(user_id=tl_id)
        if user:
            await self._delete_cached_user(user)

        return team

    async def select_team_by_id(self, team_id: UUID) -> TeamEntity | None:
        return await self.store.select_team_by_id(team_id)

    async def select_teams(self, offset: int = 0, limit: int = 10) -> list[TeamEntity]:
        return await self.store.select_teams(offset, limit)

    async def _get_cached_user(
        self,
        user_id: UUID | None = None,
        username: str | None = None,
    ) -> UserEntity | None:
        data: str | None = None

        if user_id:
            data = await self.cache.get(f"user/{str(user_id)}")
        elif not data and username:
            data = await self.cache.get(f"user/{username}")

        if not data:
            return None

        return self._json_to_user(data)

    async def _cache_user(self, user: UserEntity) -> UserEntity:
        data = self._user_to_json(user)

        await self.cache.save(f"user/{str(user.id)}", data)
        await self.cache.save(f"user/{user.identity.username}", data)

        return user

    async def _delete_cached_user(self, user: UserEntity) -> None:
        await self.cache.delete(f"user/{str(user.id)}")
        await self.cache.delete(f"user/{user.identity.username}")

    def _user_to_json(self, user: UserEntity) -> str:
        data = user.model_dump()
        data["identity"]["password"] = user.identity.password.get_secret_value()
        data["id"] = str(data["id"])
        data["teams"] = {str(key): value.value for key, value in user.teams.items()}

        return json.dumps(data, default=str)

    def _json_to_user(self, data: str) -> UserEntity | None:
        try:
            dict_data = json.loads(data)
            return UserEntity(
                id=dict_data["id"],
                identity=UserIdentity(
                    username=dict_data["identity"]["username"],
                    password=dict_data["identity"]["password"],
                ),
                info=UserInfo(
                    first_name=dict_data["info"]["first_name"],
                    second_name=dict_data["info"]["second_name"],
                ),
                teams={
                    UUID(key): Role(value) for key, value in dict_data["teams"].items()
                },
            )
        except ValidationError:
            return None
