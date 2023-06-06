FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl libyaml-dev \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ARG POETRY_HOME=/etc/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python - --version 1.2.2
ENV PATH="${PATH}:${POETRY_HOME}/bin"

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --without=dev --no-interaction

COPY ./main.py ./
COPY ./app /app
COPY ./tests /tests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
