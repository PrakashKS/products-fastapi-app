"""
Unit tests for ProductService.
Tests business logic without database dependencies.
"""

import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime

from app.services.product_service import ProductService
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.exceptions.product_exceptions import (
    ProductNotFoundException,
    ProductAlreadyDeletedException,
)


@pytest.mark.unit
class TestProductService:
    """Unit tests for ProductService class."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create ProductService instance with mock repository."""
        return ProductService(mock_repository)

    @pytest.fixture
    def sample_product(self):
        """Create a sample product for testing."""
        return Product(
            id=uuid4(),
            name="Test Product",
            description="Test Description",
            category="Electronics",
            price=99.99,
            stock=100,
        )

    async def test_create_product_success(self, service, mock_repository):
        """Test successful product creation."""
        product_data = ProductCreate(
            name="New Product",
            description="New Description",
            category="Books",
            price=29.99,
            stock=50,
        )

        mock_repository.create.return_value = Product(
            name=product_data.name,
            description=product_data.description,
            category=product_data.category,
            price=product_data.price,
            stock=product_data.stock,
        )

        result = await service.create_product(product_data)

        assert result.name == product_data.name
        assert result.price == product_data.price
        assert result.stock == product_data.stock
        mock_repository.create.assert_called_once()

    async def test_get_product_by_id_success(
        self, service, mock_repository, sample_product
    ):
        """Test successful product retrieval by ID."""
        mock_repository.find_by_id.return_value = sample_product

        result = await service.get_product_by_id(sample_product.id)

        assert result.id == sample_product.id
        assert result.name == sample_product.name
        mock_repository.find_by_id.assert_called_once_with(sample_product.id)

    async def test_get_product_by_id_not_found(self, service, mock_repository):
        """Test product retrieval when product doesn't exist."""
        product_id = uuid4()
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ProductNotFoundException):
            await service.get_product_by_id(product_id)

    async def test_get_product_by_id_deleted(
        self, service, mock_repository, sample_product
    ):
        """Test product retrieval when product is deleted."""
        sample_product.soft_delete()
        mock_repository.find_by_id.return_value = sample_product

        with pytest.raises(ProductAlreadyDeletedException):
            await service.get_product_by_id(sample_product.id)

    async def test_get_all_products(self, service, mock_repository, sample_product):
        """Test retrieving all products."""
        products = [sample_product]
        mock_repository.find_all.return_value = products

        result = await service.get_all_products()

        assert len(result) == 1
        assert result[0].id == sample_product.id
        mock_repository.find_all.assert_called_once_with(include_deleted=False)

    async def test_update_product_success(
        self, service, mock_repository, sample_product
    ):
        """Test successful product update."""
        update_data = ProductUpdate(name="Updated Name", price=149.99)
        mock_repository.find_by_id.return_value = sample_product
        mock_repository.update.return_value = sample_product

        result = await service.update_product(sample_product.id, update_data)

        assert result.name == "Updated Name"
        assert result.price == 149.99
        mock_repository.update.assert_called_once()

    async def test_update_product_not_found(self, service, mock_repository):
        """Test product update when product doesn't exist."""
        product_id = uuid4()
        update_data = ProductUpdate(name="Updated Name")
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ProductNotFoundException):
            await service.update_product(product_id, update_data)

    async def test_update_product_deleted(
        self, service, mock_repository, sample_product
    ):
        """Test product update when product is deleted."""
        sample_product.soft_delete()
        update_data = ProductUpdate(name="Updated Name")
        mock_repository.find_by_id.return_value = sample_product

        with pytest.raises(ProductAlreadyDeletedException):
            await service.update_product(sample_product.id, update_data)

    async def test_delete_product_success(
        self, service, mock_repository, sample_product
    ):
        """Test successful product soft deletion."""
        mock_repository.find_by_id.return_value = sample_product
        mock_repository.update.return_value = sample_product

        result = await service.delete_product(sample_product.id)

        assert result.is_deleted()
        assert result.deleted_at is not None
        mock_repository.update.assert_called_once()

    async def test_delete_product_not_found(self, service, mock_repository):
        """Test product deletion when product doesn't exist."""
        product_id = uuid4()
        mock_repository.find_by_id.return_value = None

        with pytest.raises(ProductNotFoundException):
            await service.delete_product(product_id)

    async def test_delete_product_already_deleted(
        self, service, mock_repository, sample_product
    ):
        """Test product deletion when product is already deleted."""
        sample_product.soft_delete()
        mock_repository.find_by_id.return_value = sample_product

        with pytest.raises(ProductAlreadyDeletedException):
            await service.delete_product(sample_product.id)
