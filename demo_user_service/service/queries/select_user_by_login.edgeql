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

} filter .deleted = false and .login = <str>$login limit 1;