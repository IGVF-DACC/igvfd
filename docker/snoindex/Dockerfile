FROM python:3.11.15-slim-trixie

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV VIRTUAL_ENV=/opt/venv

# Optional: trust an extra CA certificate during build (e.g. a sandboxed or
# corporate TLS-intercepting proxy). No-op when EXTRA_CA_CERT_B64 is unset.
ARG EXTRA_CA_CERT_B64
RUN if [ -n "$EXTRA_CA_CERT_B64" ]; then \
    echo "$EXTRA_CA_CERT_B64" | base64 -d > /usr/local/share/ca-certificates/extra-ca.crt \
    && update-ca-certificates \
    && pip config set --global global.cert /etc/ssl/certs/ca-certificates.crt; \
    fi

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
