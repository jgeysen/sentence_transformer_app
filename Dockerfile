ARG PYTHON_VERSION=3.9.17
FROM python:${PYTHON_VERSION}-slim-bookworm as dev_image

ARG POETRY_VERSION=1.4.2

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

COPY pyproject.toml poetry.lock $PYSETUP_PATH/

RUN apt-get update && apt-get -y install curl \
    && cd $PYSETUP_PATH \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2 --yes \
    && poetry install

#RUN rm -rf ~/.cache \
#    && rm -rf /var/lib/apt/lists/*
