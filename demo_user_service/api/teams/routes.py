from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Response

from demo_user_service.api.common import (
    FilterQuery,
    PersistentStoreDep,
    RequestAuthorDep,
    RequestAuthorIdDep,
)
from demo_user_service.core import NotFoundObjectError, Role, TeamInfo
from demo_user_service.core.errors import NotEnoughRightsError
from demo_user_service.core.predicates import has_role_in_team

from .contracts import CreateTeamRequest, TeamResponse

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("")
async def post_teams(
    body: CreateTeamRequest,
    store: PersistentStoreDep,
    author: RequestAuthorIdDep,
) -> TeamResponse:
    entity = await store.insert_team(
        info=TeamInfo(title=body.title, description=body.description),
        tl_id=author,
    )

    return TeamResponse.from_entity(entity)


@router.get("/{team_id}")
async def get_teams_by_id(
    team_id: UUID,
    store: PersistentStoreDep,
    _: RequestAuthorIdDep,
) -> TeamResponse:
    entity = await store.select_team_by_id(team_id=team_id)

    if not entity:
        raise NotFoundObjectError(f"team [{team_id}]")

    return TeamResponse.from_entity(entity)


@router.get("")
async def get_teams(
    filter: FilterQuery,
    store: PersistentStoreDep,
    _: RequestAuthorIdDep,
) -> list[TeamResponse]:
    entities = await store.select_teams(offset=filter.offset, limit=filter.limit)

    return [TeamResponse.from_entity(entity) for entity in entities]


@router.post(
    "/{team_id}/users/{user_id}/add",
    response_model=None,
)
async def post_teams_users_add(
    author: RequestAuthorDep,
    store: PersistentStoreDep,
    team_id: UUID,
    user_id: UUID,
    role: Annotated[Role, Query()] = Role.SDE,
):
    if not has_role_in_team(user=author, team_id=team_id, role=Role.TL):
        raise NotEnoughRightsError(
            f"user [{author.id}] has not enough rights to perform action:"
            f"add user [{user_id}] to team [{team_id}]"
        )

    await store.add_user_to_team(user_id=user_id, team_id=team_id, role=role)
    return Response()


@router.post(
    "/{team_id}/users/{user_id}/change",
    response_model=None,
)
async def post_teams_users_change(
    author: RequestAuthorDep,
    store: PersistentStoreDep,
    team_id: UUID,
    user_id: UUID,
    role: Annotated[Role, Query()],
):
    if not has_role_in_team(user=author, team_id=team_id, role=Role.TL):
        raise NotEnoughRightsError(
            f"user [{author.id}] has not enough rights to perform action:"
            f"change user [{user_id}] role in team [{team_id}]"
        )

    await store.update_user_role_in_team(user_id=user_id, team_id=team_id, role=role)
    return Response()


@router.post(
    "/{team_id}/users/{user_id}/remove",
    response_model=None,
)
async def post_teams_users_remove(
    author: RequestAuthorDep,
    store: PersistentStoreDep,
    team_id: UUID,
    user_id: UUID,
):
    if not has_role_in_team(user=author, team_id=team_id, role=Role.TL):
        raise NotEnoughRightsError(
            f"user [{author.id}] has not enough rights to perform action:"
            f"remove user [{user_id}] from team [{team_id}]"
        )

    await store.remove_user_from_team(user_id=user_id, team_id=team_id)
    return Response()
