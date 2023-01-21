FROM python:3.9 as requirements

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN curl -sSL https://install.python-poetry.org -o install-poetry.py

RUN python install-poetry.py --yes

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9

WORKDIR /app

ENV PORT=8080

COPY --from=requirements /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN rm requirements.txt

RUN playwright install --with-deps

COPY ./ /app/

CMD uvicorn --workers 1 --env-file .env.prod --port 8080 --host 0.0.0.0 bot:app
