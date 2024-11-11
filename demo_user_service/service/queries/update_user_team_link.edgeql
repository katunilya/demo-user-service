update User
filter .id = <uuid>$user_id
set {
    teams := (
        select .teams {
            @role := <UserRole>$role
        }
        filter .id = <uuid>$team_id
    )
};