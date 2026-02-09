"""
Product service layer.
Contains business logic for product operations.
"""

from typing import List
from uuid import UUID

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.exceptions.product_exceptions import (
    ProductNotFoundException,
    ProductAlreadyDeletedException,
    ProductValidationException,
)
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """
    Service layer for product business logic.
    Orchestrates operations between routers and repositories.
    """

    def __init__(self, repository: ProductRepository):
        """
        Initialize service with repository.
        
        Args:
            repository: Product repository instance
        """
        self.repository = repository

    async def create_product(self, product_data: ProductCreate) -> Product:
        """
        Create a new product.
        
        Args:
            product_data: Product creation data
            
        Returns:
            Created product
            
        Raises:
            ProductValidationException: If validation fails
        """
        # Additional business logic validation can be added here
        product = Product(
            name=product_data.name,
            description=product_data.description,
            category=product_data.category,
            price=product_data.price,
            stock=product_data.stock,
        )
        
        return await self.repository.create(product)

    async def get_product_by_id(self, product_id: UUID) -> Product:
        """
        Get a product by ID.
        
        Args:
            product_id: Product UUID
            
        Returns:
            Product instance
            
        Raises:
            ProductNotFoundException: If product not found
            ProductAlreadyDeletedException: If product is deleted
        """
        product = await self.repository.find_by_id(product_id)
        
        if not product:
            raise ProductNotFoundException(str(product_id))
        
        if product.is_deleted():
            raise ProductAlreadyDeletedException(str(product_id))
        
        return product

    async def get_all_products(self) -> List[Product]:
        """
        Get all active (non-deleted) products.
        
        Returns:
            List of active products
        """
        products = await self.repository.find_all(include_deleted=False)
        return products

    async def update_product(
        self, product_id: UUID, product_data: ProductUpdate
    ) -> Product:
        """
        Update a product.
        
        Args:
            product_id: Product UUID
            product_data: Product update data
            
        Returns:
            Updated product
            
        Raises:
            ProductNotFoundException: If product not found
            ProductAlreadyDeletedException: If product is deleted
        """
        product = await self.repository.find_by_id(product_id)
        
        if not product:
            raise ProductNotFoundException(str(product_id))
        
        if product.is_deleted():
            raise ProductAlreadyDeletedException(str(product_id))
        
        # Update only provided fields
        update_data = product_data.model_dump(exclude_unset=True)
        product.update(
            name=update_data.get("name"),
            description=update_data.get("description"),
            category=update_data.get("category"),
            price=update_data.get("price"),
            stock=update_data.get("stock"),
        )
        
        return await self.repository.update(product)

    async def delete_product(self, product_id: UUID) -> Product:
        """
        Soft delete a product.
        
        Args:
            product_id: Product UUID
            
        Returns:
            Soft-deleted product
            
        Raises:
            ProductNotFoundException: If product not found
            ProductAlreadyDeletedException: If product already deleted
        """
        product = await self.repository.find_by_id(product_id)
        
        if not product:
            raise ProductNotFoundException(str(product_id))
        
        if product.is_deleted():
            raise ProductAlreadyDeletedException(str(product_id))
        
        product.soft_delete()
        return await self.repository.update(product)
