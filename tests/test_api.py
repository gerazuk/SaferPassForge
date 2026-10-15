"""Integration tests for the presentation and REST API layer."""

from fastapi.testclient import TestClient


def test_should_return_200_ok_on_health_check(client: TestClient) -> None:
    """Arrange: Use configured TestClient.
    Act: Send GET request to /api/v1/health.
    Assert: Response status is 200 OK and contains application metadata.
    """
    # Act
    response = client.get("/api/v1/health")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "SaferPassForge"
    assert "env" in data


def test_should_generate_password_return_201_and_never_store_plaintext_in_history(
    client: TestClient,
) -> None:
    """Arrange: Prepare a valid PasswordGenerateRequest payload.
    Act: Send POST request to /api/v1/passwords/generate.
    Assert:
        - Status code is 201 Created.
        - Response contains valid password metadata and calculated entropy.
        - Plaintext password is never exposed in the audit history.
    """
    # Arrange
    payload = {
        "length": 20,
        "use_uppercase": True,
        "use_lowercase": True,
        "use_digits": True,
        "use_symbols": True,
        "exclude_ambiguous": False,
        "context_label": "Production Vault",
    }

    # Act
    post_response = client.post("/api/v1/passwords/generate", json=payload)

    # Assert
    assert post_response.status_code == 201
    result = post_response.json()
    assert result["length"] == 20
    assert len(result["password"]) == 20
    assert result["context_label"] == "Production Vault"
    assert result["entropy_bits"] > 80.0
    assert result["strength_category"] == "Very Strong"
    assert "*" in result["masked_preview"]

    # Security Assertion: Query audit history and verify plaintext is not present
    history_response = client.get("/api/v1/passwords/history")
    assert history_response.status_code == 200
    history_items = history_response.json()
    assert len(history_items) == 1

    audit_entry = history_items[0]
    assert "password" not in audit_entry
    assert audit_entry["context_label"] == "Production Vault"
    assert audit_entry["masked_preview"] == result["masked_preview"]


def test_should_persist_and_retrieve_audit_history_from_database(
    client: TestClient,
) -> None:
    """Arrange: Generate multiple passwords with distinct context labels.
    Act: Fetch the history list endpoint with a limit.
    Assert: History records are persisted in SQLite and ordered from newest to oldest.
    """
    # Arrange: Generate 3 passwords
    for i in range(3):
        client.post(
            "/api/v1/passwords/generate",
            json={"length": 16, "context_label": f"Service-{i}"},
        )

    # Act
    history_response = client.get("/api/v1/passwords/history?limit=2")

    # Assert
    assert history_response.status_code == 200
    items = history_response.json()
    assert len(items) == 2
    # Verify newest first (Service-2, then Service-1)
    assert items[0]["context_label"] == "Service-2"
    assert items[1]["context_label"] == "Service-1"


def test_should_clear_audit_history_and_return_204_no_content(
    client: TestClient,
) -> None:
    """Arrange: Generate passwords to populate the database.
    Act: Send DELETE request to /api/v1/passwords/history.
    Assert: Status is 204 No Content and subsequent history GET returns an empty list.
    """
    # Arrange
    client.post(
        "/api/v1/passwords/generate",
        json={"length": 16, "context_label": "Temporary"},
    )

    # Act
    delete_response = client.delete("/api/v1/passwords/history")

    # Assert
    assert delete_response.status_code == 204

    # Verify history is now empty
    history_response = client.get("/api/v1/passwords/history")
    assert history_response.status_code == 200
    assert len(history_response.json()) == 0


def test_should_serve_web_interface_html_at_root_path(client: TestClient) -> None:
    """Arrange: Use configured TestClient.
    Act: Send GET request to root path '/'.
    Assert: Status is 200 OK and response contains HTML title and application markup.
    """
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text
    assert "SaferPassForge" in response.text
