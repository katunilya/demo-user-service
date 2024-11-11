from edgedb import EdgeDBError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import ValidationError

from demo_user_service.core import AppError

from . import teams, users
from .common import (
    APIConfig,
    app_error_handler,
    edgedb_error_handler,
    expired_signature_error_handler,
    jwt_claims_error_handler,
    jwt_error_handler,
    request_validation_error_handler,
    startup_and_shutdown,
    validation_error_handler,
)


def create_app() -> FastAPI:
    config = APIConfig()

    app = FastAPI(
        debug=config.DEBUG,
        title=config.TITLE,
        description=config.DESCRIPTION,
        version=config.VERSION,
        lifespan=startup_and_shutdown,
    )

    # add exception handlers
    app.add_exception_handler(JWTError, jwt_error_handler)
    app.add_exception_handler(ExpiredSignatureError, expired_signature_error_handler)
    app.add_exception_handler(JWTClaimsError, jwt_claims_error_handler)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(EdgeDBError, edgedb_error_handler)

    # add routers
    app.include_router(users.router)
    app.include_router(teams.router)

    # add prometheus
    Instrumentator(
        excluded_handlers=["/metrics", "/openapi.json", "/docs"],
    ).instrument(app).expose(app)

    return app
