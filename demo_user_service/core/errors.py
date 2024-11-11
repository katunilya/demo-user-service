from http import HTTPStatus


class AppError(Exception):
    status: int = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str) -> None:
        self.message = message


class NotEnoughRightsError(AppError):
    status = HTTPStatus.FORBIDDEN


class NotFoundObjectError(AppError):
    status = HTTPStatus.NOT_FOUND


class InvalidPasswordError(AppError):
    status = HTTPStatus.UNAUTHORIZED
