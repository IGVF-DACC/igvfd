FROM public.ecr.aws/docker/library/golang:1.21.5-bookworm AS builder

ARG VERSION=v0.1.7

WORKDIR /build

RUN git clone -b ${VERSION} --depth 1 https://github.com/keenangraham/go-sqs-deduplication.git .

RUN CGO_ENABLED=0 go build -ldflags="-X 'main.Version=${VERSION}'" -o dedup cmd/dedup.go

FROM public.ecr.aws/ubuntu/ubuntu:23.10_stable

RUN useradd -m dedup

WORKDIR /app

COPY --chown=dedup:dedup *.sh .

RUN chmod +x *.sh

COPY --from=builder /build/dedup .

RUN chmod +x dedup

USER dedup

ENTRYPOINT ["./entrypoint.sh"]

CMD ["./run-once.sh"]
