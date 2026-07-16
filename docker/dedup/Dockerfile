FROM public.ecr.aws/docker/library/golang:1.21.5-bookworm AS builder

# Optional: trust an extra CA certificate during build (e.g. a sandboxed or
# corporate TLS-intercepting proxy). No-op when EXTRA_CA_CERT_B64 is unset.
ARG EXTRA_CA_CERT_B64
RUN if [ -n "$EXTRA_CA_CERT_B64" ]; then \
    echo "$EXTRA_CA_CERT_B64" | base64 -d > /usr/local/share/ca-certificates/extra-ca.crt \
    && update-ca-certificates; \
    fi

ARG VERSION=v2.0.0

WORKDIR /build

RUN git clone -b ${VERSION} --depth 1 https://github.com/IGVF-DACC/go-sqs-deduplication.git .

RUN CGO_ENABLED=0 go build -ldflags="-X 'main.Version=${VERSION}'" -o dedup cmd/dedup.go

FROM public.ecr.aws/ubuntu/ubuntu:24.04_stable

RUN apt-get update \
    && apt-get install -y ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m dedup

WORKDIR /app

COPY --chown=dedup:dedup *.sh .

RUN chmod +x *.sh

COPY --from=builder /build/dedup .

RUN chmod +x dedup

USER dedup

ENTRYPOINT ["./entrypoint.sh"]

CMD ["./run-once.sh"]
