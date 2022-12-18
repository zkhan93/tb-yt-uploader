FROM python:3.10-alpine
RUN apk add --update --no-cache ffmpeg

RUN apk add --update --no-cache gcc libffi-dev libc-dev
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1
ENV PATH="$PATH:$POETRY_HOME/bin"
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry

#RUN curl -sSL https://install.python-poetry.org | python3

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry install  --no-root --no-interaction --no-ansi
COPY . /code/
ENTRYPOINT [ "sh" ]
CMD ["scripts/start-bot.sh"]

