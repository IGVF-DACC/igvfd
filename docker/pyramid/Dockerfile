FROM python:3.9.9-buster

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv

ENV REFERENCE_DATABASE_DIRECTORY=/srv/sqlite

RUN useradd -u 1444 -m igvfd

RUN apt-get update

RUN apt-get install -y make git curl graphviz

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN chown -R igvfd:igvfd $VIRTUAL_ENV

RUN mkdir -p $REFERENCE_DATABASE_DIRECTORY

RUN chown -R igvfd:igvfd $REFERENCE_DATABASE_DIRECTORY

WORKDIR /scripts

COPY --chown=igvfd:igvfd scripts .

RUN chmod -R +x /scripts

WORKDIR /igvfd

COPY --chown=igvfd:igvfd setup.cfg pyproject.toml ./

COPY --chown=igvfd:igvfd src/igvfd/__init__.py src/igvfd/__init__.py

USER igvfd

RUN python -m pip install --upgrade pip

RUN pip install -e .[test]

COPY --chown=igvfd:igvfd src/igvfd/schema_formats.py src/igvfd/schema_formats.py

COPY --chown=igvfd:igvfd src/igvfd/ontology.py src/igvfd/ontology.py

COPY --chown=igvfd:igvfd assets/ontology.json.gz assets/ontology.json.gz

COPY --chown=igvfd:igvfd src/igvfd/commands/make_reference_db.py src/igvfd/commands/make_reference_db.py

RUN make-reference-db

COPY --chown=igvfd:igvfd . .

EXPOSE 6543

ENTRYPOINT ["/scripts/pyramid/entrypoint.sh"]

CMD ["/scripts/pyramid/run-production.sh"]
