FROM python:3.9.9-buster

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update

RUN apt-get install -y make git curl

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip

WORKDIR /docker

COPY ./config/docker_compose/pyramid/entrypoint.sh .

RUN chmod +x ./entrypoint.sh

WORKDIR /igvfd

COPY setup.cfg pyproject.toml .

COPY src/igvfd/__init__.py src/igvfd/__init__.py

RUN pip install -e .[test]

COPY . .

ENTRYPOINT ["/docker/entrypoint.sh"]