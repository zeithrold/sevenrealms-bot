FROM python:3.9 as requirements

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN curl -sSL https://install.python-poetry.org -o install-poetry.py
RUN python install-poetry.py --yes

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM ubuntu:focal as venv

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y python3.9 python3.9-venv python3.9-dev git build-essential

WORKDIR /app/

RUN python3.9 -m venv venv

ENV PATH="/app/venv/bin:${PATH}"

COPY --from=requirements /tmp/requirements.txt /app/requirements.txt

RUN pip install -Ur requirements.txt

FROM mcr.microsoft.com/playwright:v1.29.1-focal

WORKDIR /app/

RUN apt-get update
RUN apt-get install -y python3.9 python3.9-venv

COPY --from=venv /app /app

ENV PORT=8080
ENV PATH="/app/venv/bin:${PATH}"
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY ./ /app/

CMD uvicorn --workers 1 --env-file .env.prod --port 8080 --host 0.0.0.0 bot:app
