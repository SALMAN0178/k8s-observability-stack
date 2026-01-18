# Kubernetes Full-Stack Observability Pipeline

## 🚀 Overview
This repository contains a complete observability solution deployed on a K3s cluster. It demonstrates the end-to-end flow of telemetry data—from a custom-instrumented Python application to a centralized Grafana dashboard.

## 🏗️ Architecture
The system follows a modern observability pattern:
1. **Application**: Flask-based web app instrumented with Prometheus client libraries.
2. **Collection**: OpenTelemetry (OTel) Collector configured with custom receivers and exporters.
3. **Storage**: Prometheus server acting as the time-series database.
4. **Visualization**: Grafana dashboarding using PromQL for real-time monitoring.

## 🌟 Skills Demonstrated

**Cloud Native Orchestration: Managing K8s resources (Namespaces, Pods, NodePort Services, and RBAC).
**Application Instrumentation: Implementing custom Prometheus metrics (Counters, Histograms) within a Python/Flask runtime.
**Telemetry Pipelines: Configuring OpenTelemetry (OTel) collectors for multi-source data ingestion.
**Advanced PromQL: Utilizing rate functions, aggregation operators, and label filtering for high-fidelity visualization.
**System Debugging: Analyzing container logs, resolving volume mount permissions, and troubleshooting network port-binding conflicts.

## 🛠️ Deployment Steps
To deploy this stack in your own cluster, run the manifests in the following order:

1. **Setup Namespace & RBAC:**
   `kubectl apply -f manifests/otel-rbac-ns.yaml`
2. **Deploy Application:**
   `kubectl apply -f manifests/python-app.yaml`
   `kubectl apply -f manifests/python-nodeport-svc.yaml`
3. **Deploy OTel Collector:**
   `kubectl apply -f manifests/otel-collector-config.yaml`
   `kubectl apply -f manifests/otel-collector-daemonset.yaml`

## 🔍 Troubleshooting & Engineering Challenges
This project involved significant real-world debugging, which served as a deep dive into Kubernetes internals:

* **HostPath Permissions**: Resolved `Permission Denied` errors by aligning container volume mounts with host-level Ubuntu user permissions (`/home/ze/app.py`).
* **OTel YAML Validation**: Debugged "Invalid Key" errors in the OTel Collector by refactoring the `kubeletstats` receiver to match version-specific schema requirements.
* **Metric Windowing**: Optimized Grafana visualization by shifting from raw counters to `rate()` functions over a 1m/5m sliding window to provide accurate traffic insights.

## 📊 Custom PromQL Dashboard
The final dashboard includes a custom panel monitoring **Requests Per Second (RPS)**:
`sum(rate(http_requests_total[5m])) by (endpoint)`
## 📊 Final Dashboard Overview

The following screenshots demonstrate the operational state of the cluster. By utilizing PromQL, I transformed raw metrics into high-level business insights:

* **Service Reliability:** The "App Status" panel provides an instant binary view of pod health (Up/Down).
* **Traffic Analysis:** The multi-colored bar gauges allow for granular tracking of request distribution across different API endpoints.
* **Real-time Throughput:** The time-series graph calculates the request rate per second, enabling us to monitor for traffic spikes or anomalies.
<img width="1024" height="680" alt="Screenshot (18)" src="https://github.com/user-attachments/assets/3eb8fb72-99dd-4a8c-8f99-535b9e07e6e8" />
<img width="1024" height="687" alt="Screenshot (17)" src="https://github.com/user-attachments/assets/9eb237aa-290c-4361-9a40-27d2d5085242" />
