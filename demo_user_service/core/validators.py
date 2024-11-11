from pydantic import SecretStr, ValidationInfo
from pydantic_core.core_schema import WithInfoValidatorFunction


def has_special_symbols(value: str | SecretStr, info: ValidationInfo) -> SecretStr:
    _value = value if isinstance(value, str) else value.get_secret_value()

    if any(c.isalnum() for c in _value):
        return SecretStr(_value)

    raise ValueError(f"{info.field_name} must contain special symbols")


def has_numbers(count: int = 1) -> WithInfoValidatorFunction:
    def _validation_function(value: str | SecretStr, info: ValidationInfo) -> SecretStr:
        _value = value if isinstance(value, str) else value.get_secret_value()

        if sum(1 if c.isdigit() else 0 for c in _value) >= count:
            return SecretStr(_value)

        raise ValueError(f"{info.field_name} must contain at least {count} digits")

    return _validation_function


def longer_than(length: int) -> WithInfoValidatorFunction:
    def _validation_function(value: str | SecretStr, info: ValidationInfo) -> SecretStr:
        _value = value if isinstance(value, str) else value.get_secret_value()

        if len(_value) >= length:
            return SecretStr(_value)

        raise ValueError(f"{info.field_name} must be longer than {length} symbols")

    return _validation_function
