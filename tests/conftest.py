"""
Pytest configuration and fixtures.
"""

import asyncio
from typing import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.database import db
from app.config import get_settings


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    """
    Setup test database connection.
    Uses a separate test database to avoid conflicts with production data.
    """
    settings = get_settings()
    test_db_name = f"{settings.mongodb_database}_test"
    
    # Connect to test database using class attributes (Database.get_collection checks class attrs)
    db.__class__.client = AsyncIOMotorClient(settings.mongodb_url)
    database = db.__class__.client[test_db_name]
    db.__class__.collection = database[settings.mongodb_collection]

    # Create indexes
    await db.__class__.collection.create_index("id", unique=True)
    await db.__class__.collection.create_index("category")
    await db.__class__.collection.create_index("deletedAt")

    yield db

    # Cleanup: Drop test database after tests and reset class attributes
    await db.__class__.client.drop_database(test_db_name)
    db.__class__.client.close()
    db.__class__.client = None
    db.__class__.collection = None


@pytest.fixture
async def client(test_db) -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async HTTP client for testing API endpoints.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_product_data():
    """
    Provide sample product data for testing.
    """
    return {
        "name": "Test Product",
        "description": "This is a test product",
        "category": "Electronics",
        "price": 99.99,
        "stock": 100,
    }


@pytest.fixture
def sample_product_update_data():
    """
    Provide sample product update data for testing.
    """
    return {
        "name": "Updated Product",
        "price": 149.99,
        "stock": 50,
    }
