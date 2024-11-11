module default {
    scalar type UserRole extending enum<TL, SDE, SRE, QA>;

    type Team {
        required title: str;
        description: str;

        multi members := .<teams[is User];
    }

    type User {
        required login: str {
            constraint exclusive;
        };
        required first_name: str;
        required second_name: str;
        required password: str;
        required deleted: bool {
            default := false;
        };

        multi teams: Team {
            role: UserRole;
        }
    }
}
