from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import jwt
from passlib.context import CryptContext
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from demo_user_service.core.models import UserEntity


class AuthConfig(BaseSettings):
    JWT_SECRET: SecretStr = "super_secret_string"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int | None = None
    CRYPT_SCHEME: str = "bcrypt"

    model_config = {
        "env_prefix": "AUTH_",
    }


@dataclass(slots=True)
class AuthService:
    config: AuthConfig

    _crypt_context: CryptContext = field(init=False)

    def __post_init__(self) -> None:
        self._crypt_context = CryptContext(
            schemes=[self.config.CRYPT_SCHEME],
            deprecated="auto",
        )

    def encode_token_for_user(
        self,
        user: UserEntity,
    ) -> str:
        claims = {"sub": str(user.id)}
        if self.config.JWT_EXPIRE_MINUTES is not None:
            claims["exp"] = datetime.now(tz=UTC) + timedelta(
                minutes=self.config.JWT_EXPIRE_MINUTES
            )
        return jwt.encode(
            claims=claims,
            key=self.config.JWT_SECRET.get_secret_value(),
            algorithm=self.config.JWT_ALGORITHM,
        )

    def decode_user_id_from_token(
        self,
        token: str,
    ) -> UUID:
        return UUID(
            jwt.decode(
                token=token,
                key=self.config.JWT_SECRET.get_secret_value(),
                algorithms=[self.config.JWT_ALGORITHM],
            )["sub"]
        )

    def secure_password(
        self,
        password: SecretStr,
    ) -> SecretStr:
        return SecretStr(
            self._crypt_context.hash(
                secret=password.get_secret_value(),
            )
        )

    def passwords_match(
        self,
        password: SecretStr,
        hashed_password: SecretStr,
    ) -> bool:
        return self._crypt_context.verify(
            secret=password.get_secret_value(),
            hash=hashed_password.get_secret_value(),
        )
