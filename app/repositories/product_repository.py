"""
Product repository for database operations.
Implements the repository pattern for data access.
"""

from typing import List, Optional
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection

from app.models.product import Product
from app.exceptions.product_exceptions import DatabaseException


class ProductRepository:
    """
    Repository for product data access operations.
    Handles all database interactions for products.
    """

    def __init__(self, collection: AsyncIOMotorCollection):
        """
        Initialize repository with MongoDB collection.
        
        Args:
            collection: MongoDB collection for products
        """
        self.collection = collection

    async def create(self, product: Product) -> Product:
        """
        Create a new product in the database.
        
        Args:
            product: Product instance to create
            
        Returns:
            Created product
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            document = product.to_dict()
            await self.collection.insert_one(document)
            return product
        except Exception as e:
            raise DatabaseException(f"Failed to create product: {str(e)}")

    async def find_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        Find a product by ID.
        
        Args:
            product_id: Product UUID
            
        Returns:
            Product if found, None otherwise
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            document = await self.collection.find_one({"id": str(product_id)})
            if document:
                document.pop("_id", None)  # Remove MongoDB's _id field
                return Product.from_dict(document)
            return None
        except Exception as e:
            raise DatabaseException(f"Failed to find product: {str(e)}")

    async def find_all(self, include_deleted: bool = False) -> List[Product]:
        """
        Find all products.
        
        Args:
            include_deleted: Whether to include soft-deleted products
            
        Returns:
            List of products
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            query = {} if include_deleted else {"deletedAt": None}
            cursor = self.collection.find(query)
            documents = await cursor.to_list(length=None)
            
            products = []
            for doc in documents:
                doc.pop("_id", None)  # Remove MongoDB's _id field
                products.append(Product.from_dict(doc))
            
            return products
        except Exception as e:
            raise DatabaseException(f"Failed to find products: {str(e)}")

    async def update(self, product: Product) -> Product:
        """
        Update an existing product.
        
        Args:
            product: Product instance with updated data
            
        Returns:
            Updated product
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            document = product.to_dict()
            await self.collection.update_one(
                {"id": str(product.id)}, {"$set": document}
            )
            return product
        except Exception as e:
            raise DatabaseException(f"Failed to update product: {str(e)}")

    async def delete(self, product_id: UUID) -> bool:
        """
        Hard delete a product (permanently remove from database).
        This is typically not used in favor of soft delete.
        
        Args:
            product_id: Product UUID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            DatabaseException: If database operation fails
        """
        try:
            result = await self.collection.delete_one({"id": str(product_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise DatabaseException(f"Failed to delete product: {str(e)}")

    async def exists(self, product_id: UUID) -> bool:
        """
        Check if a product exists.
        
        Args:
            product_id: Product UUID
            
        Returns:
            True if exists, False otherwise
        """
        try:
            count = await self.collection.count_documents({"id": str(product_id)})
            return count > 0
        except Exception as e:
            raise DatabaseException(f"Failed to check product existence: {str(e)}")
