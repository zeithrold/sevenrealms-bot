FROM python:3.9 as requirements

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN curl -sSL https://install.python-poetry.org -o install-poetry.py

RUN python install-poetry.py --yes

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM mcr.microsoft.com/playwright:v1.29.1-focal

RUN apt update

RUN apt-get install -y git build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv

ENV PYENV_ROOT="${HOME}/.pyenv"

ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

ENV PYTHON_VERSION=3.9

RUN pyenv install ${PYTHON_VERSION} && pyenv global ${PYTHON_VERSION}

WORKDIR /app

ENV PORT=8080

COPY --from=requirements /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN rm requirements.txt

ENV PLAYWRIGHT_BROWSERS_PATH /ms-playwright

COPY ./ /app/

CMD uvicorn --workers 1 --env-file .env.prod --port 8080 --host 0.0.0.0 bot:app
