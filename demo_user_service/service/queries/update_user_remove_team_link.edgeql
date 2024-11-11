update User
filter .id = <uuid>$user_id
set {
    teams -= (
        select detached Team
        filter .id = <uuid>$team_id
    )
};