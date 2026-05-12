# Kubernetes Self-Healing Platform

A project demonstrating a Kubernetes-deployed FastAPI service with self-healing behavior through Kubernetes probes and resource configuration.

## Project Overview

This repository contains:
- `app/`: FastAPI application code, Dockerfile, and Python dependencies
- `k8s/`: Kubernetes manifests for deployment and service
- `helm/`: Helm chart directory for packaging and deploying the application (if used)
- `monitoring/`: Monitoring-related resources and integrations
- `scripts/` and `terraform/`: auxiliary deployment and infrastructure automation files

## Application

The FastAPI app exposes:
- `GET /` - returns a basic health response with pod hostname
- `GET /health` - returns `{"status": "ok"}` for Kubernetes liveness/readiness checks
- `GET /stress` - generates CPU load for testing

### `app/main.py`
- Uses FastAPI to expose endpoints
- Uses `socket.gethostname()` to identify the running pod
- Includes a stress route for workload simulation

## Docker

The application is containerized using the `app/Dockerfile`.

### Build locally

```bash
cd app
docker build -t self-healing-app:v1 .
```

### Run locally

```bash
docker run --rm -p 5001:5001 self-healing-app:v1
```

Then visit `http://localhost:5001/`.

## Kubernetes Deployment

The Kubernetes manifests are in `k8s/`.

### Deployment

`k8s/deployment.yaml` defines:
- `Deployment` named `self-healing-app`
- `replicas: 5`
- container image `self-healing-app:v1`
- resource requests/limits for CPU and memory
- `livenessProbe` and `readinessProbe` on `/health`

### Service

`k8s/service.yaml` defines:
- `Service` named `self-healing-service`
- `NodePort` type
- target port `5001`
- node port `30080`

### Apply manifests

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Access the app

If running on a local Kubernetes cluster, access the service at:

```bash
http://<node-ip>:30080/
```

## Health and Self-Healing

Kubernetes self-healing is enabled through:
- `livenessProbe` on `/health`
- `readinessProbe` on `/health`
- resource `requests`/`limits`

If a pod becomes unhealthy, Kubernetes will restart it automatically.

## Dependencies

Python dependencies are listed in `app/requirements.txt` and include:
- `fastapi`
- `uvicorn`
- `pydantic`
- `starlette`

## Development

Install dependencies and run the app locally:

```bash
cd app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 5001
```

## Repository Structure

```text
README.md
app/
  Dockerfile
  main.py
  requirements.txt
docs/
helm/
k8s/
  deployment.yaml
  service.yaml
monitoring/
screenshots/
scripts/
terraform/
```

## Notes

- The container image is referenced as `self-healing-app:v1` in the manifest. Update this if you push a new image tag.
- The NodePort service uses `30080`, which may require cluster node firewall/port access.
- The `/stress` endpoint can be used to exercise the app under load and observe Kubernetes behavior.

## License

This project is provided for demonstration and portfolio use.
