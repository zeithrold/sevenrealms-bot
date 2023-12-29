FROM python:3.11 as venv

WORKDIR /app

RUN python -m venv venv

ENV PATH="/app/venv/bin:${PATH}"

ADD requirements.txt /app/requirements.txt

RUN pip install -Ur requirements.txt

FROM python:3.11

WORKDIR /app/

COPY --from=venv /app /app

ENV TZ=Asia/Shanghai
ENV PORT=8080
ENV PATH="/app/venv/bin:${PATH}"

# RUN playwright install
# RUN playwright install-deps

COPY ./ /app/

CMD nb datastore upgrade && uvicorn --workers 1 --env-file .env.prod --port 8080 --host 0.0.0.0 bot:app
