from fastapi.testclient import TestClient

from backend.api.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "RAGForge"
    assert data["version"] == "0.1.0"


def test_query_validation():
    response = client.post(
        "/query",
        json={"query": "What is RAG?"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["query"] == "What is RAG?"


def test_empty_query_rejected():
    response = client.post(
        "/query",
        json={"query": ""}
    )

    assert response.status_code == 422
