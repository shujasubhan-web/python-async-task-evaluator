import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "Python Async Evaluator"}

def test_evaluate_task_success():
    payload = {
        "task_name": "QuickSort Benchmark",
        "execution_time": 0.5,
        "memory_mb": 128.0
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Passed"
    assert data["performance_score"] > 60.0

def test_evaluate_task_exceed_limit():
    payload = {
        "task_name": "Heavy Loop Test",
        "execution_time": 15.0,
        "memory_mb": 512.0
    }
    response = client.post("/evaluate", json=payload)
    assert response.status_code == 400
