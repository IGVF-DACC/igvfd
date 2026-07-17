import logging
import os


class _DropContextDetachNoise(logging.Filter):
    """
    Drop the 'Failed to detach context' LookupError tracebacks that the
    Pyramid/WSGI instrumentation emits for every snovault subrequest
    (upstream contrib issue; spans and trace correlation are unaffected).
    Genuine attach/exporter errors are not filtered.
    """

    def filter(self, record):
        return 'Failed to detach context' not in record.getMessage()


def is_otel_enabled():
    return os.environ.get('OTEL_ENABLED', 'false').lower() in ('true', '1', 'yes')


def configure_opentelemetry():
    """
    Set up the OpenTelemetry SDK and auto-instrumentation for one process.

    Must run per worker (gunicorn post_fork), never in the pre-fork master:
    the BatchSpanProcessor exporter thread does not survive a fork. With
    `gunicorn --paste` and no preload_app the Pyramid app is loaded after
    post_fork, so instrumentors registered here patch in time.
    """
    logging.getLogger('opentelemetry.context').addFilter(_DropContextDetachNoise())

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    # Resource.create() and OTLPSpanExporter() read OTEL_SERVICE_NAME,
    # OTEL_EXPORTER_OTLP_ENDPOINT and OTEL_EXPORTER_OTLP_HEADERS from the
    # environment (set in docker-compose.otel.yml).
    provider = TracerProvider(resource=Resource.create())
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)

    from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
    from opentelemetry.instrumentation.pyramid import PyramidInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

    PyramidInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    BotocoreInstrumentor().instrument()
    # opensearch-py has no dedicated instrumentation; its requests surface
    # here as urllib3 client spans against opensearch:9200.
    URLLib3Instrumentor().instrument()
