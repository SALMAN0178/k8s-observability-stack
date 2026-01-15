# app.py
from flask import Flask, request
from prometheus_client import Counter, generate_latest, Histogram
import time

app = Flask(__name__)

# Custom Metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total number of requests to the application',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

@app.route('/')
def home():
    REQUEST_COUNT.labels(method=request.method, endpoint='/').inc()
    return "Hello, OpenTelemetry World! Metrics are exposed on /metrics"

@app.route('/slow')
def slow():
    start_time = time.time()
    time.sleep(0.5) 
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint='/slow').observe(latency)
    REQUEST_COUNT.labels(method=request.method, endpoint='/slow').inc()
    return f"Request took {latency:.2f} seconds."

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    from prometheus_client import start_http_server
    # Metrics served on port 8000
    start_http_server(8000) 
    # Web app served on port 5000
    app.run(host='0.0.0.0', port=5000)
