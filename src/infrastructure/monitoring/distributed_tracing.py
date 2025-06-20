import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from celery.signals import worker_process_init
import logging

logger = logging.getLogger(__name__)

def init_tracing(app, db_engine=None, celery_app=None):
    """
    初始化OpenTelemetry分布式追踪。
    """
    # 定义资源，例如服务名称
    resource = Resource.create({
        "service.name": os.getenv("OTEL_SERVICE_NAME", "jewelry-recommendation-backend"),
        "service.version": os.getenv("APP_VERSION", "1.0.0"),
    })

    # 使用OTLP导出器替代Jaeger导出器
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"),
        insecure=os.getenv("OTEL_EXPORTER_OTLP_INSECURE", "true").lower() == "true",
    )

    # 配置 TracerProvider
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)
    logger.info("OpenTelemetry TracerProvider initialized with OTLP exporter.")

    # 自动注入 Flask 应用
    try:
        FlaskInstrumentor().instrument_app(app)
        logger.info("Flask auto-instrumentation enabled.")
    except ImportError:
        logger.warning("Flask auto-instrumentation not available. Please install opentelemetry-instrumentation-flask.")

    # 自动注入 SQLAlchemy 数据库操作
    if db_engine:
        try:
            SQLAlchemyInstrumentor().instrument(engine=db_engine)
            logger.info("SQLAlchemy auto-instrumentation enabled.")
        except ImportError:
            logger.warning("SQLAlchemy auto-instrumentation not available. Please install opentelemetry-instrumentation-sqlalchemy.")

    # 自动注入 Celery Worker
    if celery_app:
        try:
            # Celery使用prefork模型，每个worker进程需要独立初始化OpenTelemetry SDK
            @worker_process_init.connect(weak=False)
            def init_celery_worker_tracing(*args, **kwargs):
                CeleryInstrumentor().instrument()
                # 确保每个worker进程都有自己的TracerProvider实例
                worker_provider = TracerProvider(resource=resource)
                worker_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
                trace.set_tracer_provider(worker_provider)
                logger.info("Celery worker auto-instrumentation enabled.")
        except ImportError:
            logger.warning("Celery auto-instrumentation not available. Please install opentelemetry-instrumentation-celery.")
