FROM python:3.12 AS base

ARG PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=500 \
    POETRY_VERSION=1.8.4

RUN apt-get update && apt-get install -y gcc
RUN python -m pip install --upgrade pip
RUN python -m pip install "poetry==$POETRY_VERSION"


WORKDIR $APP_ROOT/src
COPY . ./

ENV BASH_ENV= \
    ENV= \
    PROMPT_COMMAND=

ENV VIRTUAL_ENV=$APP_ROOT/src/.venv \
    PATH=$APP_ROOT/src/.venv/bin:$PATH


RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.path --unset \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi
