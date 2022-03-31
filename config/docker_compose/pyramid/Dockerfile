FROM python:3.9.9-buster

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv

RUN apt-get update

RUN apt-get install -y make git curl graphviz

RUN python -m venv $VIRTUAL_ENV

RUN groupadd -g 1001 igvfd

RUN useradd -g 1001 -m igvfd

RUN chown -R igvfd:igvfd $VIRTUAL_ENV

USER igvfd

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip

WORKDIR /docker

COPY --chown=igvfd:igvfd ./config/docker_compose/pyramid/entrypoint.sh .

RUN chmod +x ./entrypoint.sh

WORKDIR /igvfd

COPY --chown=igvfd:igvfd setup.cfg pyproject.toml ./

COPY --chown=igvfd:igvfd src/igvfd/__init__.py src/igvfd/__init__.py

RUN pip install -e .[test]

COPY --chown=igvfd:igvfd . .

ENTRYPOINT ["/docker/entrypoint.sh"]
