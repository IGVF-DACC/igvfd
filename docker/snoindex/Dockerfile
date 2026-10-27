FROM python:3.11.17-slim-trixie

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv

RUN useradd -u 1444 -m snoindex

RUN mkdir -p /snovault-index

RUN chown -R snoindex:snoindex /snovault-index

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN chown -R snoindex:snoindex $VIRTUAL_ENV

WORKDIR /snovault-index

COPY --chown=snoindex:snoindex requirements.txt ./

USER snoindex

RUN echo "pip==26.2.2 --hash=sha256:fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70" > /tmp/pip-bootstrap.txt \
    && python -m pip install --require-hashes -r /tmp/pip-bootstrap.txt \
    && rm /tmp/pip-bootstrap.txt

RUN pip install -r requirements.txt
