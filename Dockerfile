ARG PYTHON_VERSION=3.9.17

FROM python:${PYTHON_VERSION}-slim-bookworm as base_image

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=off
ENV PATH="$POETRY_HOME/bin:$PATH"

ARG ROOT_DIR=/project
WORKDIR ${ROOT_DIR}

COPY pyproject.toml poetry.lock $ROOT_DIR/

RUN apt-get update && apt-get -y install curl \
    && cd $ROOT_DIR \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2 --yes \
    && poetry install --no-dev \
    && poetry shell

FROM base_image as prod_image

COPY ./ ${ROOT_DIR}/

FROM base_image as dev_image

RUN poetry install
