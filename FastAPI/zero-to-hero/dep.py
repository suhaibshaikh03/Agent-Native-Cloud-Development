"""
Simple example demonstrating dependency injection in FastAPI.

This file shows how to use FastAPI's dependency injection system
with various patterns including simple dependencies, cached dependencies,
and yield dependencies for resource cleanup.
"""

from fastapi import FastAPI, Depends, HTTPException
from typing import Optional
from functools import lru_cache
import uuid
from datetime import datetime


app = FastAPI(title="Dependency Injection Example")


# 1. Simple dependency function
def get_current_user():
    """Simple dependency that returns current user information."""
    return {"username": "john_doe", "id": 123, "role": "user"}


@app.get("/simple")
def simple_example(current_user: dict = Depends(get_current_user)):
    """Example endpoint using simple dependency."""
    return {
        "message": "Hello from simple dependency example",
        "user": current_user
    }


# 2. Dependency with parameters
def get_query_params(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    """Dependency that extracts and validates query parameters."""
    return {
        "q": q,
        "skip": skip,
        "limit": limit
    }


@app.get("/with-params")
def with_params_example(params: dict = Depends(get_query_params)):
    """Example endpoint using dependency with parameters."""
    return {
        "message": "Example with query parameters",
        "params": params
    }


# 3. Cached dependency using lru_cache
@lru_cache
def get_settings():
    """Cached dependency for application settings.

    This dependency is expensive to compute once,
    so we cache it using lru_cache decorator.
    """
    print("Loading settings...")  # This will only print once
    return {
        "app_name": "My FastAPI App",
        "version": "1.0.0",
        "debug": True,
        "max_items": 100
    }


@app.get("/cached")
def cached_example(settings: dict = Depends(get_settings)):
    """Example endpoint using cached dependency."""
    return {
        "message": "Example with cached settings",
        "settings": settings
    }


# 4. Yield dependency for resource cleanup
def get_temp_resource():
    """Dependency that provides a temporary resource and cleans it up.

    Uses yield to provide resource during request processing
    and cleanup code after the request is complete.
    """
    print("Creating temporary resource...")
    resource_id = str(uuid.uuid4())

    try:
        # Yield the resource to the endpoint
        yield {"id": resource_id, "created_at": datetime.now()}
    finally:
        # Cleanup code that runs after the endpoint completes
        print(f"Cleaning up temporary resource: {resource_id}")


@app.get("/yield")
def yield_example(temp_resource: dict = Depends(get_temp_resource)):
    """Example endpoint using yield dependency."""
    return {
        "message": "Example with yield dependency",
        "resource": temp_resource
    }


# 5. Dependency chain - one dependency depends on another
def get_config():
    """Base configuration dependency."""
    return {
        "app_name": "Chained Example",
        "api_version": "v1"
    }


def get_logger(config: dict = Depends(get_config)):
    """Logger dependency that depends on config."""
    import logging

    logger = logging.getLogger(config["app_name"])
    logger.setLevel(logging.INFO)

    return {
        "logger": logger,
        "app_name": config["app_name"]
    }


@app.get("/chained")
def chained_example(logger_info: dict = Depends(get_logger)):
    """Example endpoint using chained dependencies."""
    return {
        "message": "Example with chained dependencies",
        "logger_info": logger_info
    }


# 6. Class-based dependency
class DatabaseService:
    """Class-based dependency example."""

    def __init__(self):
        self.connection_count = 0

    def get_connection(self):
        self.connection_count += 1
        return {
            "connection_id": f"conn_{self.connection_count}",
            "status": "active"
        }


# Create a single instance to share
db_service = DatabaseService()


def get_db_service():
    """Dependency that returns the database service instance."""
    return db_service


@app.get("/class-dependency")
def class_dependency_example(db: DatabaseService = Depends(get_db_service)):
    """Example endpoint using class-based dependency."""
    connection = db.get_connection()
    return {
        "message": "Example with class-based dependency",
        "connection": connection,
        "total_connections": db.connection_count
    }


# 7. Authentication example with dependency
def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Dependency that checks if user is active."""
    if current_user["role"] == "inactive":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/protected")
def protected_example(active_user: dict = Depends(get_current_active_user)):
    """Example endpoint with authentication dependency."""
    return {
        "message": "This is a protected endpoint",
        "user": active_user
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)