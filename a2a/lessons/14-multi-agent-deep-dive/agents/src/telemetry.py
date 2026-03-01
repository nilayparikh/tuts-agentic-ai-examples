"""
OpenTelemetry setup for the multi-agent loan approval pipeline.

Configure distributed tracing with OTLP export. Every agent imports
this module to get a pre-configured tracer that propagates W3C trace
context across A2A requests.

Environment variables
---------------------
  OTEL_EXPORTER_OTLP_ENDPOINT   OTLP HTTP endpoint (default: http://localhost:4318)
  OTEL_SERVICE_NAME              Service name for traces (default: loan-approval)
"""

from __future__ import annotations

import os
from typing import Any

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)


def setup_telemetry(service_name: str | None = None) -> trace.Tracer:
    """Initialise OpenTelemetry tracing and return a Tracer.

    Falls back to console export if no OTLP endpoint is reachable.
    """
    svc = service_name or os.getenv("OTEL_SERVICE_NAME", "loan-approval")
    resource = Resource.create({"service.name": svc})
    provider = TracerProvider(resource=resource)

    # OTLP exporter (Jaeger / Grafana Tempo / any OTLP collector)
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if otlp_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

    # Always add console exporter for local development visibility
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
    return trace.get_tracer(svc)


def inject_trace_context() -> dict[str, str]:
    """Return W3C traceparent headers for propagation to downstream agents."""
    from opentelemetry.propagate import (
        inject,
    )  # pylint: disable=import-outside-toplevel

    headers: dict[str, str] = {}
    inject(headers)
    return headers


def extract_trace_context(headers: dict[str, Any]) -> trace.context.Context | None:
    """Extract W3C trace context from incoming request headers."""
    from opentelemetry.propagate import (
        extract,
    )  # pylint: disable=import-outside-toplevel

    return extract(headers)


# Module-level tracer — import this in agent modules
tracer = setup_telemetry()
