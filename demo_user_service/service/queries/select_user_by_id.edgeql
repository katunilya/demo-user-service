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

} filter .deleted = false and .id = <uuid>$user_id limit 1;