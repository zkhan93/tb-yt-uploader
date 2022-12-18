# FROM linuxserver/ffmpeg:latest
FROM ubuntu:22.04
# FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# RUN apt-get update && \
#     apt-get install -y software-properties-common && \
#     add-apt-repository -y ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt install -y python3.10

RUN apt-get update && apt-get install -y ffmpeg python3 python3-pip curl &&\
    rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1
ENV PATH="$PATH:$POETRY_HOME/bin"
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry --version

WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN ls $POETRY_HOME
RUN poetry install  --no-root --no-interaction --no-ansi
COPY . /code/
ENTRYPOINT [ "bash" ]
CMD ["scripts/start-bot.sh"]

