from fastapi.testclient import TestClient
from main import app
import pytest
# Create a test client instance
client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint that returns 'Hello World'.
    This test verifies that the GET request to "/" returns the expected response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    print("✓ Root endpoint test passed!")


def test_create_user():
    """
    Test the user creation endpoint with Pydantic validation.
    This test verifies that POST request to "/users" creates a user with proper validation.
    """
    # Test data that matches the UserCreateRequest model
    user_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 30,
        "tags": ["developer", "python"]
    }

    response = client.post("/users", json=user_data)

    # Check that the response status is successful
    assert response.status_code == 200

    # Check that the response contains the expected fields
    response_data = response.json()
    assert "id" in response_data
    assert response_data["name"] == user_data["name"]
    assert response_data["email"] == user_data["email"]
    assert response_data["age"] == user_data["age"]
    assert response_data["tags"] == user_data["tags"]
    assert "created_at" in response_data

    print("✓ User creation test passed!")


def test_create_user_validation_error():
    """
    Test the user creation endpoint with invalid data to check Pydantic validation.
    This test verifies that the API properly validates input and returns error for invalid data.
    """
    # Invalid data - incorrect email format
    invalid_user_data = {
        "name": "John Doe",
        "email": "invalid-email",  # Invalid email format
        "age": 30,
        "tags": ["developer", "python"]
    }

    response = client.post("/users", json=invalid_user_data)

    # Check that the response status is 422 (validation error)
    assert response.status_code == 422

    print("✓ User validation error test passed!")


def test_search_endpoint():
    """
    Test the search endpoint with query parameters.
    This test verifies that GET request to "/search" works with query parameters.
    """
    response = client.get("/search", params={"query": "python", "limit": 10})

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["query"] == "python"
    assert response_data["limit"] == 10
    assert "message" in response_data

    print("✓ Search endpoint test passed!")


def test_get_user_by_id_success():
    """
    Test the user retrieval endpoint with a valid user ID.
    This test verifies that GET request to "/users/{id}" returns the correct user.
    """
    response = client.get("/users/123")

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["id"] == 123
    assert response_data["name"] == "Charlie Brown"
    assert response_data["email"] == "charlie@example.com"

    print("✓ Get user by ID success test passed!")


def test_get_user_by_id_not_found():
    """
    Test the user retrieval endpoint with an invalid user ID.
    This test verifies that GET request to "/users/{id}" returns 404 for non-existent user.
    """
    response = client.get("/users/999")

    assert response.status_code == 404

    response_data = response.json()
    assert "detail" in response_data
    assert "User with ID 999 not found" in response_data["detail"]

    print("✓ Get user by ID not found test passed!")


def test_admin_endpoint_unauthorized():
    """
    Test the admin endpoint without proper authentication.
    This test verifies that the admin endpoint returns 401 when no token is provided.
    """
    response = client.get("/admin")

    assert response.status_code == 401

    response_data = response.json()
    assert "detail" in response_data
    assert "Authentication token required" in response_data["detail"]

    print("✓ Admin endpoint unauthorized test passed!")


def test_admin_endpoint_forbidden():
    """
    Test the admin endpoint with invalid authentication token.
    This test verifies that the admin endpoint returns 403 when invalid token is provided.
    """
    response = client.get("/admin", headers={"X-Token": "invalid-token"})

    assert response.status_code == 403

    response_data = response.json()
    assert "detail" in response_data
    assert "Access forbidden: Invalid token" in response_data["detail"]

    print("✓ Admin endpoint forbidden test passed!")


def test_admin_endpoint_success():
    """
    Test the admin endpoint with valid authentication token.
    This test verifies that the admin endpoint returns success with valid token.
    """
    response = client.get("/admin", headers={"X-Token": "admin-secret"})

    assert response.status_code == 200

    response_data = response.json()
    assert "message" in response_data
    assert "Admin data accessed successfully" in response_data["message"]

    print("✓ Admin endpoint success test passed!")


def test_validate_email_success():
    """
    Test the email validation endpoint with a valid email.
    This test verifies that the email validation endpoint accepts valid emails.
    """
    response = client.get("/validate-email", params={"email": "test@example.com"})

    assert response.status_code == 200

    response_data = response.json()
    assert "message" in response_data
    assert "test@example.com" in response_data["message"]

    print("✓ Email validation success test passed!")


def test_validate_email_error():
    """
    Test the email validation endpoint with an invalid email.
    This test verifies that the email validation endpoint returns 422 for invalid emails.
    """
    response = client.get("/validate-email", params={"email": "invalid-email"})

    assert response.status_code == 422

    response_data = response.json()
    assert "detail" in response_data
    assert "Invalid email format" in response_data["detail"]

    print("✓ Email validation error test passed!")


if __name__ == "__main__":
    # Run the tests when this script is executed directly
    test_read_root()
    test_create_user()
    test_create_user_validation_error()
    test_search_endpoint()
    test_get_user_by_id_success()
    test_get_user_by_id_not_found()
    test_admin_endpoint_unauthorized()
    test_admin_endpoint_forbidden()
    test_admin_endpoint_success()
    test_validate_email_success()
    test_validate_email_error()
    print("\nAll tests passed successfully! 🎉")