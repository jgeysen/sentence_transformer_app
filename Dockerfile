FROM python:3.9.17-slim-bookworm as base_image

ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=off \
    VENV_PATH="/project/.venv" \
    ROOT_DIR="/project"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR ${ROOT_DIR}
COPY ./ ${ROOT_DIR}/

SHELL ["/bin/bash", "-c"]
RUN echo "source ${VENV_PATH}/bin/activate" >> $HOME/.bashrc

RUN apt-get update && apt-get -y install curl \
    && cd $ROOT_DIR \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2 --yes \
    && poetry install --no-dev

FROM base_image as dev_image

RUN poetry install
