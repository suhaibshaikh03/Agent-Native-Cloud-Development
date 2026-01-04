from fastapi import FastAPI

app = FastAPI()

# ROOT ENDPOINT
# How to use in search bar: http://localhost:8000/
# Description: Returns a simple "Hello World" message
# Method: GET
# Parameters: None
# Returns: JSON object with a message
@app.get("/")
def read_root() -> dict:
    "slash route"
    return {"message": "Hello World"}

# USER ENDPOINT WITH INTEGER PATH PARAMETER
# How to use in search bar: http://localhost:8000/users/{user_id}
# Example: http://localhost:8000/users/123
# Description: Retrieves information about a specific user by their ID
# Method: GET
# Parameters: user_id (integer) - the unique identifier for the user
# Returns: JSON object containing the user ID and a message
@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict:
    """
    Get a user by ID.
    Path parameter: user_id (integer)
    """
    return {"user_id": user_id, "message": f"User with ID {user_id}"}

# ITEM ENDPOINT WITH STRING PATH PARAMETER
# How to use in search bar: http://localhost:8000/items/{item_name}
# Example: http://localhost:8000/items/laptop
# Description: Retrieves information about a specific item by its name
# Method: GET
# Parameters: item_name (string) - the name of the item to retrieve
# Returns: JSON object containing the item name and a message
@app.get("/items/{item_name}")
def get_item(item_name: str) -> dict:
    """
    Get an item by name.
    Path parameter: item_name (string)
    """
    return {"item_name": item_name, "message": f"Item with name {item_name}"}

# NESTED ENDPOINT WITH MULTIPLE PATH PARAMETERS
# How to use in search bar: http://localhost:8000/users/{user_id}/items/{item_id}
# Example: http://localhost:8000/users/123/items/book456
# Description: Retrieves a specific item for a specific user
# Method: GET
# Parameters:
#   - user_id (integer) - the unique identifier for the user
#   - item_id (string) - the identifier for the item
# Returns: JSON object containing both IDs and a descriptive message
@app.get("/users/{user_id}/items/{item_id}")
def get_user_item(user_id: int, item_id: str) -> dict:
    """
    Get a specific item for a specific user.
    Path parameters: user_id (integer), item_id (string)
    """
    return {
        "user_id": user_id,
        "item_id": item_id,
        "message": f"Item {item_id} for user {user_id}"
    }

# FILE PATH ENDPOINT WITH PATH VALIDATION
# How to use in search bar: http://localhost:8000/files/{file_path}
# Example: http://localhost:8000/files/documents/readme.txt
# Description: Retrieves information about a file at a specific path
# Method: GET
# Parameters: file_path (string with path validation) - the file path to retrieve
# Returns: JSON object containing the file path and a message
@app.get("/files/{file_path:path}")
def get_file(file_path: str) -> dict:
    """
    Get a file with path validation.
    Path parameter: file_path (with path validation)
    """
    return {"file_path": file_path, "message": f"File path: {file_path}"}

# USER PROFILE ENDPOINT WITH PREDEFINED VALUES
# How to use in search bar: http://localhost:8000/users/{user_id}/profile/{profile_type}
# Example: http://localhost:8000/users/123/profile/detailed
# Valid profile types: "basic", "detailed", "full"
# Description: Retrieves a specific type of profile for a user
# Method: GET
# Parameters:
#   - user_id (integer) - the unique identifier for the user
#   - profile_type (string) - the type of profile to retrieve (must be one of: "basic", "detailed", "full")
# Returns: JSON object containing user ID, profile type, and a descriptive message
# Error: If an invalid profile type is provided, returns an error message with valid types
@app.get("/users/{user_id}/profile/{profile_type}")
def get_user_profile(user_id: int, profile_type: str) -> dict:
    """
    Get user profile of a specific type.
    Path parameters: user_id (integer), profile_type (string)
    """
    valid_types = ["basic", "detailed", "full"]
    if profile_type not in valid_types:
        return {
            "error": f"Invalid profile type. Valid types: {valid_types}",
            "user_id": user_id,
            "profile_type": profile_type
        }
    return {
        "user_id": user_id,
        "profile_type": profile_type,
        "message": f"{profile_type.title()} profile for user {user_id}"
    }