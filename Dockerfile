FROM python:3.9 as venv

WORKDIR /app

RUN python -m venv venv

ENV PATH="/app/venv/bin:${PATH}"

ADD requirements.txt /app/requirements.txt

RUN pip install -Ur requirements.txt

FROM python:3.9

WORKDIR /app/

COPY --from=venv /app /app

ENV PORT=8080
ENV PATH="/app/venv/bin:${PATH}"

COPY ./ /app/

CMD uvicorn --workers 1 --env-file .env.prod --port 8080 --host 0.0.0.0 bot:app
