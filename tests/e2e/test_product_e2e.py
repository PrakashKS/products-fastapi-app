"""
End-to-end tests using Playwright.
Tests the complete user workflow through the API.
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, APIRequestContext


@pytest.mark.e2e
class TestProductE2E:
    """End-to-end tests for Product API using Playwright."""

    @pytest.fixture(scope="class")
    async def api_context(self):
        """Create Playwright API request context."""
        async with async_playwright() as playwright:
            context = await playwright.request.new_context(
                base_url="http://localhost:8000"
            )
            yield context
            await context.dispose()

    @pytest.mark.asyncio
    async def test_complete_product_lifecycle(self, api_context: APIRequestContext):
        """
        Test the complete product lifecycle:
        1. Create a product
        2. Verify it appears in the list
        3. Get product details
        4. Update the product
        5. Delete the product
        6. Verify it's removed from the list
        """
        # 1. Create a product
        create_response = await api_context.post(
            "/api/v1/products",
            data={
                "name": "E2E Test Product",
                "description": "Testing complete workflow",
                "category": "Testing",
                "price": 99.99,
                "stock": 50,
            },
        )
        assert create_response.status == 201
        product_data = await create_response.json()
        product_id = product_data["id"]
        assert product_data["name"] == "E2E Test Product"

        # 2. Verify it appears in the list
        list_response = await api_context.get("/api/v1/products")
        assert list_response.status == 200
        list_data = await list_response.json()
        assert list_data["total"] >= 1
        product_ids = [p["id"] for p in list_data["products"]]
        assert product_id in product_ids

        # 3. Get product details
        get_response = await api_context.get(f"/api/v1/products/{product_id}")
        assert get_response.status == 200
        get_data = await get_response.json()
        assert get_data["id"] == product_id
        assert get_data["name"] == "E2E Test Product"

        # 4. Update the product
        update_response = await api_context.put(
            f"/api/v1/products/{product_id}",
            data={
                "name": "Updated E2E Product",
                "price": 149.99,
            },
        )
        assert update_response.status == 200
        update_data = await update_response.json()
        assert update_data["name"] == "Updated E2E Product"
        assert update_data["price"] == 149.99

        # 5. Delete the product
        delete_response = await api_context.delete(f"/api/v1/products/{product_id}")
        assert delete_response.status == 200
        delete_data = await delete_response.json()
        assert delete_data["deletedAt"] is not None

        # 6. Verify it's removed from the list
        final_list_response = await api_context.get("/api/v1/products")
        final_list_data = await final_list_response.json()
        final_product_ids = [p["id"] for p in final_list_data["products"]]
        assert product_id not in final_product_ids

    @pytest.mark.asyncio
    async def test_multiple_products_workflow(self, api_context: APIRequestContext):
        """
        Test managing multiple products:
        1. Create multiple products
        2. Verify all appear in the list
        3. Update one product
        4. Delete one product
        5. Verify correct products remain
        """
        # 1. Create multiple products
        products = []
        for i in range(3):
            response = await api_context.post(
                "/api/v1/products",
                data={
                    "name": f"Product {i + 1}",
                    "category": "Electronics",
                    "price": 10.00 * (i + 1),
                    "stock": 10 * (i + 1),
                },
            )
            assert response.status == 201
            data = await response.json()
            products.append(data)

        # 2. Verify all appear in the list
        list_response = await api_context.get("/api/v1/products")
        list_data = await list_response.json()
        assert list_data["total"] >= 3

        # 3. Update one product
        update_response = await api_context.put(
            f"/api/v1/products/{products[0]['id']}",
            data={"price": 99.99},
        )
        assert update_response.status == 200

        # 4. Delete one product
        delete_response = await api_context.delete(
            f"/api/v1/products/{products[1]['id']}"
        )
        assert delete_response.status == 200

        # 5. Verify correct products remain
        final_list_response = await api_context.get("/api/v1/products")
        final_list_data = await final_list_response.json()
        final_product_ids = [p["id"] for p in final_list_data["products"]]

        assert products[0]["id"] in final_product_ids  # Updated product exists
        assert products[1]["id"] not in final_product_ids  # Deleted product removed
        assert products[2]["id"] in final_product_ids  # Untouched product exists

    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, api_context: APIRequestContext):
        """
        Test error handling scenarios:
        1. Create product with invalid data
        2. Get non-existent product
        3. Update non-existent product
        4. Delete non-existent product
        5. Access deleted product
        """
        # 1. Create product with invalid data (negative price)
        invalid_response = await api_context.post(
            "/api/v1/products",
            data={
                "name": "Invalid Product",
                "category": "Test",
                "price": -10.00,
                "stock": 10,
            },
        )
        assert invalid_response.status == 422  # Validation error

        # 2. Get non-existent product
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        get_response = await api_context.get(f"/api/v1/products/{fake_id}")
        assert get_response.status == 404

        # 3. Update non-existent product
        update_response = await api_context.put(
            f"/api/v1/products/{fake_id}",
            data={"name": "Updated"},
        )
        assert update_response.status == 404

        # 4. Delete non-existent product
        delete_response = await api_context.delete(f"/api/v1/products/{fake_id}")
        assert delete_response.status == 404

        # 5. Access deleted product
        # Create a product
        create_response = await api_context.post(
            "/api/v1/products",
            data={
                "name": "To Be Deleted",
                "category": "Test",
                "price": 10.00,
                "stock": 5,
            },
        )
        product_id = (await create_response.json())["id"]

        # Delete it
        await api_context.delete(f"/api/v1/products/{product_id}")

        # Try to access it
        get_deleted_response = await api_context.get(f"/api/v1/products/{product_id}")
        assert get_deleted_response.status == 410  # Gone

    @pytest.mark.asyncio
    async def test_api_documentation_endpoints(self, api_context: APIRequestContext):
        """Test that API documentation endpoints are accessible."""
        # Test health check
        health_response = await api_context.get("/health")
        assert health_response.status == 200
        health_data = await health_response.json()
        assert health_data["status"] == "healthy"

        # Test root endpoint
        root_response = await api_context.get("/")
        assert root_response.status == 200

        # Test OpenAPI docs (Swagger UI should be available)
        docs_response = await api_context.get("/docs")
        assert docs_response.status == 200

        # Test OpenAPI JSON schema
        openapi_response = await api_context.get("/openapi.json")
        assert openapi_response.status == 200
        openapi_data = await openapi_response.json()
        assert "openapi" in openapi_data
        assert "paths" in openapi_data
