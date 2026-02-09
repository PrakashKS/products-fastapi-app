"""
MongoDB database connection and management.
Uses Motor for async MongoDB operations.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Optional

from app.config import get_settings


class Database:
    """MongoDB database connection manager."""

    client: Optional[AsyncIOMotorClient] = None
    collection: Optional[AsyncIOMotorCollection] = None

    @classmethod
    async def connect_db(cls) -> None:
        """Establish connection to MongoDB."""
        settings = get_settings()
        cls.client = AsyncIOMotorClient(settings.mongodb_url)
        database = cls.client[settings.mongodb_database]
        cls.collection = database[settings.mongodb_collection]

        # Create indexes for better performance
        await cls.collection.create_index("id", unique=True)
        await cls.collection.create_index("category")
        await cls.collection.create_index("deletedAt")

        print(f"Connected to MongoDB: {settings.mongodb_database}")

    @classmethod
    async def close_db(cls) -> None:
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed")

    @classmethod
    def get_collection(cls) -> AsyncIOMotorCollection:
        """Get the products collection."""
        if cls.collection is None:
            raise RuntimeError("Database not connected. Call connect_db() first.")
        return cls.collection


# Global database instance
db = Database()
