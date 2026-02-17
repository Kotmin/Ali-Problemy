from fastapi.testclient import TestClient


def test_create_record(client: TestClient, sample_record: dict) -> None:
    response = client.post("/api/v1/records", json=sample_record)
    assert response.status_code == 201
    data = response.json()
    assert data["owner_name"] == "Ala"
    assert data["animal_name"] == "kot"
    assert data["since_date"] == "2024-10-31"
    assert "id" in data
    assert "created_at" in data


def test_create_record_whitespace_stripped(client: TestClient) -> None:
    payload = {
        "owner_name": "  Ala  ",
        "animal_name": "  kot  ",
        "since_date": "2024-10-31",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["owner_name"] == "Ala"
    assert data["animal_name"] == "kot"


def test_create_record_empty_owner(client: TestClient) -> None:
    payload = {
        "owner_name": "",
        "animal_name": "kot",
        "since_date": "2024-10-31",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422


def test_create_record_empty_animal(client: TestClient) -> None:
    payload = {
        "owner_name": "Ala",
        "animal_name": "",
        "since_date": "2024-10-31",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422


def test_create_record_whitespace_only_owner(client: TestClient) -> None:
    payload = {
        "owner_name": "   ",
        "animal_name": "kot",
        "since_date": "2024-10-31",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422


def test_create_record_invalid_date(client: TestClient) -> None:
    payload = {
        "owner_name": "Ala",
        "animal_name": "kot",
        "since_date": "not-a-date",
    }
    response = client.post("/api/v1/records", json=payload)
    assert response.status_code == 422


def test_list_records_empty(client: TestClient) -> None:
    response = client.get("/api/v1/records")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["records"] == []


def test_list_records_with_data(
    client: TestClient, sample_record: dict
) -> None:
    for i in range(3):
        record = {**sample_record, "owner_name": f"Owner{i}"}
        client.post("/api/v1/records", json=record)
    response = client.get("/api/v1/records")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["records"]) == 3


def test_list_records_pagination(
    client: TestClient, sample_record: dict
) -> None:
    for i in range(5):
        record = {**sample_record, "owner_name": f"Owner{i}"}
        client.post("/api/v1/records", json=record)
    response = client.get("/api/v1/records", params={"skip": 2, "limit": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    assert len(data["records"]) == 2


def test_list_records_filter_by_owner(
    client: TestClient, sample_record: dict
) -> None:
    client.post("/api/v1/records", json={**sample_record, "owner_name": "Ala"})
    client.post(
        "/api/v1/records", json={**sample_record, "owner_name": "Bartek"}
    )
    client.post(
        "/api/v1/records", json={**sample_record, "owner_name": "Alicja"}
    )
    response = client.get("/api/v1/records", params={"owner_name": "Al"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    for record in data["records"]:
        assert "al" in record["owner_name"].lower()


def test_get_record_success(
    client: TestClient, sample_record: dict
) -> None:
    create_resp = client.post("/api/v1/records", json=sample_record)
    record_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/records/{record_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["owner_name"] == "Ala"
    assert data["animal_name"] == "kot"


def test_get_record_not_found(client: TestClient) -> None:
    response = client.get("/api/v1/records/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Record not found"


def test_update_record_success(
    client: TestClient, sample_record: dict
) -> None:
    create_resp = client.post("/api/v1/records", json=sample_record)
    record_id = create_resp.json()["id"]
    update_payload = {"owner_name": "Bartek", "animal_name": "pies"}
    response = client.put(f"/api/v1/records/{record_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["owner_name"] == "Bartek"
    assert data["animal_name"] == "pies"
    assert data["since_date"] == "2024-10-31"


def test_update_record_partial(
    client: TestClient, sample_record: dict
) -> None:
    create_resp = client.post("/api/v1/records", json=sample_record)
    record_id = create_resp.json()["id"]
    response = client.put(
        f"/api/v1/records/{record_id}", json={"owner_name": "Bartek"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["owner_name"] == "Bartek"
    assert data["animal_name"] == "kot"


def test_update_record_not_found(client: TestClient) -> None:
    response = client.put(
        "/api/v1/records/999", json={"owner_name": "Bartek"}
    )
    assert response.status_code == 404


def test_delete_record_success(
    client: TestClient, sample_record: dict
) -> None:
    create_resp = client.post("/api/v1/records", json=sample_record)
    record_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/records/{record_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "deleted"
    get_resp = client.get(f"/api/v1/records/{record_id}")
    assert get_resp.status_code == 404


def test_delete_record_not_found(client: TestClient) -> None:
    response = client.delete("/api/v1/records/999")
    assert response.status_code == 404


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
