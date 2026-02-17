from fastapi.testclient import TestClient


def test_owner_name_too_long(client: TestClient) -> None:
    payload = {
        "owner_name": "A" * 101,
        "animal_name": "kot",
        "since_date": "2024-10-31",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422


def test_animal_name_too_long(client: TestClient) -> None:
    payload = {
        "owner_name": "Ala",
        "animal_name": "K" * 101,
        "since_date": "2024-10-31",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422


def test_missing_required_fields(client: TestClient) -> None:
    response = client.post("/api/v1/records", json={})
    assert response.status_code == 422


def test_missing_since_date(client: TestClient) -> None:
    payload = {"owner_name": "Ala", "animal_name": "kot"}
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422
