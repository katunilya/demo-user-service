CREATE MIGRATION m13tj4q2nbuph4pqeqcy3kho3y3yfd3zwtpdabvabtrfa3uhcomcba
    ONTO m166uapeqqlc67tp3ju2tbduq7cizr7v2egcz4sijkmndkshu4ugvq
{
  ALTER ABSTRACT LINK default::team_role {
      DROP PROPERTY value;
  };
  ALTER TYPE default::Team {
      DROP LINK members;
  };
  DROP ABSTRACT LINK default::team_role;
  DROP SCALAR TYPE default::UserTeamRole;
};
