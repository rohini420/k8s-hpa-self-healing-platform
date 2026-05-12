from fastapi import FastAPI
import socket

app = FastAPI(title="Kubernetes Self-Healing Platform")

@app.get("/")
def home():
    return {
        "message": "Kubernetes Self-Healing Platform",
        "pod": socket.gethostname(),
        "status": "healthy"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stress")
def stress():
    x = 0
    for i in range(10_000_000):
        x += i
    return {"status": "cpu load generated", "value": x}