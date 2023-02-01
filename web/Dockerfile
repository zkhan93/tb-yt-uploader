FROM python:3.10-slim

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		ffmpeg \
	; \
	rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1
ENV PATH="$PATH:$POETRY_HOME/bin"
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry install  --no-root --no-interaction --no-ansi
COPY . /code/
CMD ["/code/scripts/start-web.sh"]
