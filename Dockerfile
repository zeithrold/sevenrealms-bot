FROM python:3.12 as venv

WORKDIR /app

RUN python -m venv venv

RUN source venv/bin/activate

ADD requirements.txt /app/requirements.txt

RUN pip install -Ur requirements.txt

FROM python:3.12

WORKDIR /app/

COPY --from=venv /app /app

RUN source venv/bin/activate

ENV GOOGLE_APPLICATION_CREDENTIALS=firebase_credential.json
ENV TZ=Asia/Shanghai
ENV PORT=8080
COPY ./ /app/

CMD uvicorn \
    --workers 1 \
    --env-file .env.prod \
    --port 8080 \
    --host 0.0.0.0 \
    srbot.server:app
