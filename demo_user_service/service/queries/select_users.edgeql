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
}
filter .deleted = false
offset <int64>$offset
limit <int64>$limit;
