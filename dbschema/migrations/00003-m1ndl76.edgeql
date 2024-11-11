CREATE MIGRATION m1ndl76rnguszce7ol7slwruvp37nw5gz5ewab4ildyo5rc3byrima
    ONTO m13tj4q2nbuph4pqeqcy3kho3y3yfd3zwtpdabvabtrfa3uhcomcba
{
  CREATE SCALAR TYPE default::UserRole EXTENDING enum<TL, SDE, SRE, QA>;
  ALTER TYPE default::User {
      CREATE MULTI LINK teams: default::Team {
          CREATE PROPERTY user_roles: array<default::UserRole> {
              SET default := (<array<default::UserRole>>[]);
          };
      };
  };
  ALTER TYPE default::Team {
      CREATE MULTI LINK members := (.<teams[IS default::User]);
  };
};
