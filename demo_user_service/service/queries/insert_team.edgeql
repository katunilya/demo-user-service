select (update User 
filter .id = <uuid>$user_id
set {
    teams += (insert Team {
        title := <str>$title,
        description := <optional str>$description,
        @role := UserRole.TL
    })
}) {teams: {id}};