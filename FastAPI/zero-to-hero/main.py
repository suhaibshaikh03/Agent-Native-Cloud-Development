from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# ROOT ENDPOINT
# How to use in search bar: http://localhost:8000/
# Description: Returns a simple "Hello World" message
# Method: GET
# Parameters: None
# Returns: JSON object with a message
class RootResponse(BaseModel):
    """
    Pydantic model for the root endpoint response.
    This model defines the structure of the data returned by the root endpoint.
    """
    message: str
    status: str = "success"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"


@app.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    """
    Root endpoint that returns structured data using Pydantic model.
    Response follows RootResponse model structure with validation.
    """
    return RootResponse(
        message="Hello World",
        status="success",
        version="1.0.0"
    )

# COMMENTED OUT PATH PARAMETER EXAMPLES
# # USER ENDPOINT WITH INTEGER PATH PARAMETER
# # How to use in search bar: http://localhost:8000/users/{user_id}
# # Example: http://localhost:8000/users/123
# # Description: Retrieves information about a specific user by their ID
# # Method: GET
# # Parameters: user_id (integer) - the unique identifier for the user
# # Returns: JSON object containing the user ID and a message
# @app.get("/users/{user_id}")
# def get_user(user_id: int) -> dict:
#     """
#     Get a user by ID.
#     Path parameter: user_id (integer)
#     """
#     return {"user_id": user_id, "message": f"User with ID {user_id}"}

# # ITEM ENDPOINT WITH STRING PATH PARAMETER
# # How to use in search bar: http://localhost:8000/items/{item_name}
# # Example: http://localhost:8000/items/laptop
# # Description: Retrieves information about a specific item by its name
# # Method: GET
# # Parameters: item_name (string) - the name of the item to retrieve
# # Returns: JSON object containing the item name and a message
# @app.get("/items/{item_name}")
# def get_item(item_name: str) -> dict:
#     """
#     Get an item by name.
#     Path parameter: item_name (string)
#     """
#     return {"item_name": item_name, "message": f"Item with name {item_name}"}

# # NESTED ENDPOINT WITH MULTIPLE PATH PARAMETERS
# # How to use in search bar: http://localhost:8000/users/{user_id}/items/{item_id}
# # Example: http://localhost:8000/users/123/items/book456
# # Description: Retrieves a specific item for a specific user
# # Method: GET
# # Parameters:
# #   - user_id (integer) - the unique identifier for the user
# #   - item_id (string) - the identifier for the item
# # Returns: JSON object containing both IDs and a descriptive message
# @app.get("/users/{user_id}/items/{item_id}")
# def get_user_item(user_id: int, item_id: str) -> dict:
#     """
#     Get a specific item for a specific user.
#     Path parameters: user_id (integer), item_id (string)
#     """
#     return {
#         "user_id": user_id,
#         "item_id": item_id,
#         "message": f"Item {item_id} for user {user_id}"
#     }

# # FILE PATH ENDPOINT WITH PATH VALIDATION
# # How to use in search bar: http://localhost:8000/files/{file_path}
# # Example: http://localhost:8000/files/documents/readme.txt
# # Description: Retrieves information about a file at a specific path
# # Method: GET
# # Parameters: file_path (string with path validation) - the file path to retrieve
# # Returns: JSON object containing the file path and a message
# @app.get("/files/{file_path:path}")
# def get_file(file_path: str) -> dict:
#     """
#     Get a file with path validation.
#     Path parameter: file_path (with path validation)
#     """
#     return {"file_path": file_path, "message": f"File path: {file_path}"}

# # USER PROFILE ENDPOINT WITH PREDEFINED VALUES
# # How to use in search bar: http://localhost:8000/users/{user_id}/profile/{profile_type}
# # Example: http://localhost:8000/users/123/profile/detailed
# # Valid profile types: "basic", "detailed", "full"
# # Description: Retrieves a specific type of profile for a user
# # Method: GET
# # Parameters:
# #   - user_id (integer) - the unique identifier for the user
# #   - profile_type (string) - the type of profile to retrieve (must be one of: "basic", "detailed", "full")
# # Returns: JSON object containing user ID, profile type, and a descriptive message
# # Error: If an invalid profile type is provided, returns an error message with valid types
# @app.get("/users/{user_id}/profile/{profile_type}")
# def get_user_profile(user_id: int, profile_type: str) -> dict:
#     """
#     Get user profile of a specific type.
#     Path parameters: user_id (integer), profile_type (string)
#     """
#     valid_types = ["basic", "detailed", "full"]
#     if profile_type not in valid_types:
#         return {
#             "error": f"Invalid profile type. Valid types: {valid_types}",
#             "user_id": user_id,
#             "profile_type": profile_type
#         }
#     return {
#         "user_id": user_id,
#         "profile_type": profile_type,
#         "message": f"{profile_type.title()} profile for user {user_id}"
#     }

# PYDANTIC MODEL EXAMPLES
class User(BaseModel):
    """
    Pydantic model for User data validation and serialization.
    This model defines the structure and validation rules for user data.
    """
    id: int
    name: str = Field(..., min_length=2, max_length=50, description="User's full name")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Valid email address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age between 0 and 120")
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = []


class UserCreateRequest(BaseModel):
    """
    Pydantic model for creating a new user.
    This model defines the required fields when creating a user.
    """
    name: str = Field(..., min_length=2, max_length=50, description="User's full name")
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Valid email address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age between 0 and 120")
    tags: List[str] = Field(default=[], description="List of tags for the user")


class UserResponse(BaseModel):
    """
    Pydantic model for user response data.
    This model defines the structure of user data returned by the API.
    """
    id: int
    name: str
    email: str
    age: Optional[int]
    is_active: bool
    created_at: datetime
    tags: List[str]


# How to call the endpoint in the URL directly: POST request to http://localhost:8000/users with JSON body
# Example JSON body:
# {
#   "name": "John Doe",
#   "email": "john.doe@example.com",
#   "age": 30,
#   "tags": ["developer", "python"]
# }
# Description: Creates a new user with validation using Pydantic model
# Method: POST
# Request body: JSON object following UserCreateRequest model structure
# Returns: JSON object containing the created user with additional fields
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreateRequest) -> UserResponse:
    """
    Create a new user with Pydantic validation.
    Request body must match UserCreateRequest model structure.
    Response will match UserResponse model structure.
    """
    # Simulate creating a user with an auto-generated ID
    created_user = User(
        id=123,  # In a real app, this would come from a database
        **user.dict()  # Unpack the validated input data
    )
    return created_user


# How to call the endpoint in the URL directly: GET request to http://localhost:8000/user-example
# Example: http://localhost:8000/user-example
# Description: Returns an example user object demonstrating Pydantic model usage
# Method: GET
# Parameters: None
# Returns: JSON object following UserResponse model structure
@app.get("/user-example", response_model=UserResponse)
def get_user_example() -> UserResponse:
    """
    Returns an example user demonstrating Pydantic model usage.
    Response follows UserResponse model structure with validation.
    """
    example_user = User(
        id=1,
        name="Jane Smith",
        email="jane.smith@example.com",
        age=28,
        tags=["designer", "ui/ux"]
    )
    return example_user


# HTTP EXCEPTION EXAMPLES
# HTTPException is used to return error responses to clients with specific status codes and detail messages.
# It's imported from fastapi and is the standard way to handle errors in FastAPI applications.

# How to call the endpoint in the URL directly: GET request to http://localhost:8000/users/123
# Example: http://localhost:8000/users/123 (when user exists) or http://localhost:8000/users/999 (when user doesn't exist)
# Description: Retrieves a user by ID, raises 404 error if user not found
# Method: GET
# Parameters: user_id (integer path parameter)
# Returns: JSON object with user data or 404 error if not found
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int) -> UserResponse:
    """
    Get a user by ID with error handling using HTTPException.
    Raises 404 if user doesn't exist.
    """
    # Simulate a database of users
    fake_users_db = {
        1: {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "age": 25},
        2: {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "age": 35},
        123: {"id": 123, "name": "Charlie Brown", "email": "charlie@example.com", "age": 30}
    }

    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {user_id} not found",
            headers={"X-Error": "User not found in database"}
        )

    user_data = fake_users_db[user_id]
    return User(
        id=user_data["id"],
        name=user_data["name"],
        email=user_data["email"],
        age=user_data["age"]
    )


# How to call the endpoint in the URL directly: GET request to http://localhost:8000/admin with proper header
# Example: http://localhost:8000/admin (with header "X-Token": "admin-secret")
# Description: Admin-only endpoint that requires authentication token
# Method: GET
# Headers: X-Token (required) - must be "admin-secret"
# Returns: JSON object with admin data or 401/403 error if unauthorized
@app.get("/admin")
def get_admin_data(x_token: str = None) -> dict:
    """
    Admin-only endpoint demonstrating HTTPException for authentication errors.
    Raises 401 if no token provided, 403 if invalid token.
    """
    if x_token is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if x_token != "admin-secret":
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: Invalid token",
            headers={"X-Error": "Invalid admin token"}
        )

    return {
        "message": "Admin data accessed successfully",
        "data": {"admin_features": True, "permissions": ["read", "write", "delete"]}
    }


# How to call the endpoint in the URL directly: GET request to http://localhost:8000/validate-email?email=valid@example.com
# Example: http://localhost:8000/validate-email?email=invalid-email (with invalid email)
# Description: Validates an email parameter, raises 422 error if invalid format
# Method: GET
# Parameters: email (query parameter, required)
# Returns: JSON object confirming valid email or 422 error if invalid
@app.get("/validate-email")
def validate_email(email: str) -> dict:
    """
    Validates an email parameter using HTTPException for validation errors.
    Raises 422 if email format is invalid.
    """
    import re
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_pattern, email):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid email format: {email}",
            headers={"X-Error": "Email validation failed"}
        )

    return {
        "message": f"Email {email} is valid",
        "email": email
    }


# QUERY PARAMETER EXAMPLES
# How to call the endpoint in the URL directly: http://localhost:8000/search?query=python
# Example: http://localhost:8000/search?query=python&limit=10
# Description: Search endpoint with optional query and limit parameters
# Method: GET
# Parameters:
#   - query (string, required) - the search query term
#   - limit (integer, optional, default=10) - maximum number of results to return
# Returns: JSON object containing search results and parameters
@app.get("/search")
def search_items(query: str, limit: int = 10) -> dict:
    """
    Search for items with query parameters.
    Query parameters: query (string, required), limit (integer, optional)
    """
    return {
        "query": query,
        "limit": limit,
        "message": f"Searching for '{query}' with limit {limit}"
    }

# How to call the endpoint in the URL directly: http://localhost:8000/users?active=true&role=admin
# Example: http://localhost:8000/users?active=true&role=admin&page=2
# Description: Get users with filtering options
# Method: GET
# Parameters:
#   - active (boolean, optional) - filter by active status
#   - role (string, optional) - filter by user role
#   - page (integer, optional, default=1) - page number for pagination
# Returns: JSON object containing filtered users and parameters
@app.get("/users")
def get_users(active: bool = None, role: str = None, page: int = 1) -> dict:
    """
    Get users with optional query parameters.
    Query parameters: active (boolean, optional), role (string, optional), page (integer, optional)
    """
    filters = {}
    if active is not None:
        filters["active"] = active
    if role:
        filters["role"] = role

    return {
        "filters": filters,
        "page": page,
        "message": f"Getting users with filters: {filters}, page: {page}"
    }

# How to call the endpoint in the URL directly: http://localhost:8000/products?category=electronics&min_price=100&max_price=1000
# Example: http://localhost:8000/products?category=books&sort=price_asc&available=true
# Description: Get products with various filtering and sorting options
# Method: GET
# Parameters:
#   - category (string, optional) - filter by product category
#   - min_price (float, optional) - minimum price filter
#   - max_price (float, optional) - maximum price filter
#   - sort (string, optional) - sorting option (price_asc, price_desc, name)
#   - available (boolean, optional) - filter by availability
# Returns: JSON object containing products and applied filters
@app.get("/products")
def get_products(
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    sort: str = "name",
    available: bool = None
) -> dict:
    """
    Get products with multiple query parameters.
    Query parameters: category, min_price, max_price, sort, available
    """
    filters = {
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "sort": sort,
        "available": available
    }
    # Remove None values from filters
    filters = {k: v for k, v in filters.items() if v is not None}

    return {
        "filters": filters,
        "message": f"Getting products with filters: {filters}"
    }