import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "field, value",
    [
        ("owner_name", "A" * 101),
        ("animal_name", "K" * 101),
    ],
    ids=["owner_too_long", "animal_too_long"],
)
def test_name_too_long(client: TestClient, field: str, value: str) -> None:
    payload = {
        "owner_name": "Ala",
        "animal_name": "kot",
        "since_date": "2024-10-31",
    }
    payload[field] = value
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422, f"{field} over 100 chars should be rejected"


def test_missing_required_fields(client: TestClient) -> None:
    response = client.post("/api/v1/records", json={})
    assert response.status_code == 422, "empty body should be rejected"
    errors = response.json()["detail"]
    missing_fields = {e["loc"][-1] for e in errors}
    assert {"owner_name", "animal_name", "since_date"} <= missing_fields, (
        "all required fields should be reported missing"
    )


def test_missing_since_date(client: TestClient) -> None:
    payload = {"owner_name": "Ala", "animal_name": "kot"}
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422, "missing since_date should be rejected"


def test_wrong_type_for_name(client: TestClient) -> None:
    payload = {
        "owner_name": 12345,
        "animal_name": "kot",
        "since_date": "2024-10-31",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422, "non-string owner_name should be rejected"


def test_null_body(client: TestClient) -> None:
    response = client.post(
        "/api/v1/records",
        content="null",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422, "null JSON body should be rejected"
