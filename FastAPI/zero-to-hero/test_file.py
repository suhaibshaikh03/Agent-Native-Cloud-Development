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


if __name__ == "__main__":
    # Run the tests when this script is executed directly
    test_read_root()
    test_create_user()
    test_create_user_validation_error()
    test_search_endpoint()
    print("\nAll tests passed successfully! 🎉")