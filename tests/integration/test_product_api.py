"""
Integration tests for Product API endpoints.
Tests the complete API flow with a test database.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestProductAPI:
    """Integration tests for Product API endpoints."""

    async def test_create_product_success(
        self, client: AsyncClient, sample_product_data
    ):
        """Test successful product creation via API."""
        response = await client.post("/api/v1/products", json=sample_product_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_product_data["name"]
        assert data["price"] == sample_product_data["price"]
        assert data["stock"] == sample_product_data["stock"]
        assert "id" in data
        assert "createdAt" in data
        assert "updatedAt" in data
        assert data["deletedAt"] is None

    async def test_create_product_invalid_price(self, client: AsyncClient):
        """Test product creation with invalid (negative) price."""
        invalid_data = {
            "name": "Invalid Product",
            "category": "Test",
            "price": -10.00,  # Invalid: negative price
            "stock": 10,
        }

        response = await client.post("/api/v1/products", json=invalid_data)

        assert response.status_code == 422  # Validation error

    async def test_create_product_invalid_stock(self, client: AsyncClient):
        """Test product creation with invalid (negative) stock."""
        invalid_data = {
            "name": "Invalid Product",
            "category": "Test",
            "price": 10.00,
            "stock": -5,  # Invalid: negative stock
        }

        response = await client.post("/api/v1/products", json=invalid_data)

        assert response.status_code == 422  # Validation error

    async def test_get_all_products_empty(self, client: AsyncClient):
        """Test getting all products when database is empty."""
        response = await client.get("/api/v1/products")

        assert response.status_code == 200
        data = response.json()
        assert data["products"] == []
        assert data["total"] == 0

    async def test_get_all_products_with_data(
        self, client: AsyncClient, sample_product_data
    ):
        """Test getting all products with existing data."""
        # Create a product first
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        assert create_response.status_code == 201

        # Get all products
        response = await client.get("/api/v1/products")

        assert response.status_code == 200
        data = response.json()
        assert len(data["products"]) == 1
        assert data["total"] == 1
        assert data["products"][0]["name"] == sample_product_data["name"]

    async def test_get_all_products_excludes_deleted(
        self, client: AsyncClient, sample_product_data
    ):
        """Test that deleted products are excluded from list."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Delete the product
        await client.delete(f"/api/v1/products/{product_id}")

        # Get all products
        response = await client.get("/api/v1/products")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0  # Deleted product should not be included

    async def test_get_product_by_id_success(
        self, client: AsyncClient, sample_product_data
    ):
        """Test getting a specific product by ID."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Get the product
        response = await client.get(f"/api/v1/products/{product_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == sample_product_data["name"]

    async def test_get_product_by_id_not_found(self, client: AsyncClient):
        """Test getting a non-existent product."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.get(f"/api/v1/products/{fake_id}")

        assert response.status_code == 404

    async def test_get_product_by_id_deleted(
        self, client: AsyncClient, sample_product_data
    ):
        """Test getting a deleted product returns 410 Gone."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Delete the product
        await client.delete(f"/api/v1/products/{product_id}")

        # Try to get the deleted product
        response = await client.get(f"/api/v1/products/{product_id}")

        assert response.status_code == 410  # Gone

    async def test_update_product_success(
        self, client: AsyncClient, sample_product_data, sample_product_update_data
    ):
        """Test successful product update."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Update the product
        response = await client.put(
            f"/api/v1/products/{product_id}", json=sample_product_update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == sample_product_update_data["name"]
        assert data["price"] == sample_product_update_data["price"]
        assert data["stock"] == sample_product_update_data["stock"]

    async def test_update_product_partial(
        self, client: AsyncClient, sample_product_data
    ):
        """Test partial product update (only some fields)."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Partial update (only price)
        update_data = {"price": 199.99}
        response = await client.put(
            f"/api/v1/products/{product_id}", json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["price"] == 199.99
        assert data["name"] == sample_product_data["name"]  # Unchanged

    async def test_update_product_not_found(self, client: AsyncClient):
        """Test updating a non-existent product."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        update_data = {"name": "Updated"}

        response = await client.put(f"/api/v1/products/{fake_id}", json=update_data)

        assert response.status_code == 404

    async def test_update_product_deleted(
        self, client: AsyncClient, sample_product_data
    ):
        """Test updating a deleted product returns 410 Gone."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Delete the product
        await client.delete(f"/api/v1/products/{product_id}")

        # Try to update the deleted product
        update_data = {"name": "Updated"}
        response = await client.put(
            f"/api/v1/products/{product_id}", json=update_data
        )

        assert response.status_code == 410  # Gone

    async def test_delete_product_success(
        self, client: AsyncClient, sample_product_data
    ):
        """Test successful product soft deletion."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Delete the product
        response = await client.delete(f"/api/v1/products/{product_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["deletedAt"] is not None

    async def test_delete_product_not_found(self, client: AsyncClient):
        """Test deleting a non-existent product."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.delete(f"/api/v1/products/{fake_id}")

        assert response.status_code == 404

    async def test_delete_product_already_deleted(
        self, client: AsyncClient, sample_product_data
    ):
        """Test deleting an already deleted product."""
        # Create a product
        create_response = await client.post(
            "/api/v1/products", json=sample_product_data
        )
        product_id = create_response.json()["id"]

        # Delete the product
        await client.delete(f"/api/v1/products/{product_id}")

        # Try to delete again
        response = await client.delete(f"/api/v1/products/{product_id}")

        assert response.status_code == 410  # Gone

    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint."""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
