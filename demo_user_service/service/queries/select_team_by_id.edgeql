select Team {
    id,
    title,
    description,
    members: {id, @role}
}
filter .id = <uuid>$team_id limit 1;