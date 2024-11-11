import logging
from uuid import UUID

from .models import Role, UserEntity

logger = logging.getLogger(__name__)


def has_role_in_team(user: UserEntity, team_id: UUID, role: Role) -> bool:
    return team_id in user.teams and role is user.teams[team_id]
