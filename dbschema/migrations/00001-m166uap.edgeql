CREATE MIGRATION m166uapeqqlc67tp3ju2tbduq7cizr7v2egcz4sijkmndkshu4ugvq
    ONTO initial
{
  CREATE SCALAR TYPE default::UserTeamRole EXTENDING enum<TL, SDE, SRE, QA>;
  CREATE ABSTRACT LINK default::team_role {
      CREATE PROPERTY value: default::UserTeamRole;
  };
  CREATE TYPE default::User {
      CREATE REQUIRED PROPERTY deleted: std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY first_name: std::str;
      CREATE REQUIRED PROPERTY login: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY password: std::str;
      CREATE REQUIRED PROPERTY second_name: std::str;
  };
  CREATE TYPE default::Team {
      CREATE MULTI LINK members: default::User {
          EXTENDING default::team_role;
      };
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
  };
};
