select Team {
    id,
    title,
    description,
    members: {id, @role}
}
offset <int64>$offset 
limit <int64>$limit;