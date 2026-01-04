from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    "slash route"
    return {"message": "Hello World"}

# Path parameter example - single parameter
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """
    Get a user by ID.
    Path parameter: user_id (integer)
    """
    return {"user_id": user_id, "message": f"User with ID {user_id}"}

# Path parameter example - string parameter
@app.get("/items/{item_name}")
def get_item(item_name: str):
    """
    Get an item by name.
    Path parameter: item_name (string)
    """
    return {"item_name": item_name, "message": f"Item with name {item_name}"}

# Path parameter example - multiple parameters
@app.get("/users/{user_id}/items/{item_id}")
def get_user_item(user_id: int, item_id: str):
    """
    Get a specific item for a specific user.
    Path parameters: user_id (integer), item_id (string)
    """
    return {
        "user_id": user_id,
        "item_id": item_id,
        "message": f"Item {item_id} for user {user_id}"
    }

# Path parameter with validation
@app.get("/files/{file_path:path}")
def get_file(file_path: str):
    """
    Get a file with path validation.
    Path parameter: file_path (with path validation)
    """
    return {"file_path": file_path, "message": f"File path: {file_path}"}

# Path parameter with predefined values
@app.get("/users/{user_id}/profile/{profile_type}")
def get_user_profile(user_id: int, profile_type: str):
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