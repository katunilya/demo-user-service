CREATE MIGRATION m1t4tg65zh3avoq4vewotu6uctqvm2xk2svslamegacunvtmb7abrq
    ONTO m1ndl76rnguszce7ol7slwruvp37nw5gz5ewab4ildyo5rc3byrima
{
  ALTER TYPE default::User {
      ALTER LINK teams {
          DROP PROPERTY user_roles;
      };
  };
  ALTER TYPE default::User {
      ALTER LINK teams {
          CREATE PROPERTY role: default::UserRole;
      };
  };
};
