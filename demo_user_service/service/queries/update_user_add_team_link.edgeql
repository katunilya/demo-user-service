update User
filter .id = <uuid>$user_id
set {
    teams += (
        select detached Team {
            @role := <UserRole>$role
        }
        filter .id = <uuid>$team_id
    )
};