import json
from http import HTTPStatus

from edgedb import EdgeDBError
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from pydantic import ValidationError
from pydantic.alias_generators import to_snake

from demo_user_service.core.errors import AppError


def jwt_error_handler(_: Request, exc: JWTError):
    return JSONResponse(
        content={"err": "JWT_ERROR", "message": str(exc)},
        status_code=HTTPStatus.UNAUTHORIZED,
    )


def expired_signature_error_handler(_: Request, exc: ExpiredSignatureError):
    return JSONResponse(
        content={"err": "JWT_EXPIRED_SIGNATURE_ERROR", "message": str(exc)},
        status_code=HTTPStatus.UNAUTHORIZED,
    )


def jwt_claims_error_handler(_: Request, exc: JWTClaimsError):
    return JSONResponse(
        content={"err": "JWT_CLAIMS_ERROR", "message": str(exc)},
        status_code=HTTPStatus.UNAUTHORIZED,
    )


def app_error_handler(_: Request, exc: AppError):
    return JSONResponse(
        content={
            "err": to_snake(exc.__class__.__name__).upper(),
            "message": exc.message,
        },
        status_code=exc.status,
    )


def validation_error_handler(_: Request, exc: ValidationError):
    err = "VALIDATION"
    return JSONResponse(
        content={
            "err": err,
            "message": "validation error",
            "errors": [
                {
                    "description": e.get("msg"),
                    "location": e.get("loc"),
                }
                for e in json.loads(exc.json())
            ],
        },
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


def request_validation_error_handler(_: Request, exc: RequestValidationError):
    err = "VALIDATION"
    return JSONResponse(
        content={
            "err": err,
            "message": "validation error",
            "errors": [
                {
                    "description": e.get("msg"),
                    "location": e.get("loc"),
                }
                for e in exc.errors()
            ],
        },
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


def edgedb_error_handler(_: Request, exc: EdgeDBError):
    err = to_snake(exc.__class__.__name__).upper()

    return JSONResponse(
        content={
            "err": err,
            "message": str(exc),
        }
    )
