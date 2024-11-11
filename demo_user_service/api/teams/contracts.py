from __future__ import annotations

from typing import Annotated
from uuid import UUID

from pydantic import Field

from demo_user_service.api.common import CamelCaseContract
from demo_user_service.core import Role, TeamEntity


class CreateTeamRequest(CamelCaseContract):
    title: str
    description: str | None = None


class TeamResponse(CamelCaseContract):
    id: UUID
    title: str
    description: str | None = None
    members: Annotated[dict[UUID, Role], Field(default_factory=dict)]

    @staticmethod
    def from_entity(entity: TeamEntity) -> TeamResponse:
        return TeamResponse(
            id=entity.id,
            title=entity.info.title,
            description=entity.info.description,
            members=entity.members,
        )
