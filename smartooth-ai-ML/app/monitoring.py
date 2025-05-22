from flask import request
from prometheus_client import start_http_server, Counter, Gauge
import time

# Métricas Prometheus
PREDICTION_REQUESTS = Counter(
    'smartooth_prediction_requests_total',
    'Total number of prediction requests'
)

PREDICTION_TIME = Gauge(
    'smartooth_prediction_time_seconds',
    'Time taken to process predictions'
)

ACTIVE_DEVICES = Gauge(
    'smartooth_active_iot_devices',
    'Number of active IoT devices connected'
)

def init_monitoring(app):
    # Iniciar servidor de métricas
    start_http_server(8001)
    
    @app.before_request
    def before_request():
        if request.path == '/api/v1/predict':
            request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if request.path == '/api/v1/predict':
            PREDICTION_REQUESTS.inc()
            PREDICTION_TIME.set(time.time() - request.start_time)
        return response