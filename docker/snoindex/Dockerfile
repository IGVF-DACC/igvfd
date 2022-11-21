FROM python:3.9.9-slim-buster

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

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt
