"""
Products API router.
Defines all product-related endpoints.
"""

from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
    ErrorResponse,
)
from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.database import db
from app.exceptions.product_exceptions import (
    ProductNotFoundException,
    ProductAlreadyDeletedException,
    ProductValidationException,
    DatabaseException,
)


router = APIRouter(prefix="/products", tags=["Products"])


def get_product_service() -> ProductService:
    """
    Dependency injection for ProductService.
    
    Returns:
        ProductService instance
    """
    collection = db.get_collection()
    repository = ProductRepository(collection)
    return ProductService(repository)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description="Create a new product with the provided details.",
    responses={
        201: {"description": "Product created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """
    Create a new product.
    
    - **name**: Product name (required, 1-200 characters)
    - **description**: Product description (optional, max 1000 characters)
    - **category**: Product category (required, 1-100 characters)
    - **price**: Product price (required, must be positive)
    - **stock**: Stock quantity (required, must be non-negative)
    """
    try:
        product = await service.create_product(product_data)
        return ProductResponse(**product.to_dict())
    except ProductValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.get(
    "",
    response_model=ProductListResponse,
    summary="Get all products",
    description="Retrieve a list of all active (non-deleted) products.",
    responses={
        200: {"description": "Products retrieved successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_all_products(
    service: ProductService = Depends(get_product_service),
) -> ProductListResponse:
    """
    Get all active products.
    
    Returns only products that have not been soft-deleted.
    """
    try:
        products = await service.get_all_products()
        product_responses = [ProductResponse(**p.to_dict()) for p in products]
        return ProductListResponse(products=product_responses, total=len(products))
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
    description="Retrieve a specific product by its UUID.",
    responses={
        200: {"description": "Product retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Product not found"},
        410: {"model": ErrorResponse, "description": "Product has been deleted"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """
    Get a product by ID.
    
    - **product_id**: UUID of the product to retrieve
    """
    try:
        product = await service.get_product_by_id(product_id)
        return ProductResponse(**product.to_dict())
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductAlreadyDeletedException as e:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a product",
    description="Update an existing product with the provided details.",
    responses={
        200: {"description": "Product updated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        404: {"model": ErrorResponse, "description": "Product not found"},
        410: {"model": ErrorResponse, "description": "Product has been deleted"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """
    Update a product.
    
    - **product_id**: UUID of the product to update
    - **name**: Product name (optional, 1-200 characters)
    - **description**: Product description (optional, max 1000 characters)
    - **category**: Product category (optional, 1-100 characters)
    - **price**: Product price (optional, must be positive)
    - **stock**: Stock quantity (optional, must be non-negative)
    
    Only provided fields will be updated.
    """
    try:
        product = await service.update_product(product_id, product_data)
        return ProductResponse(**product.to_dict())
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductAlreadyDeletedException as e:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(e))
    except ProductValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.delete(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Delete a product (soft delete)",
    description="Soft delete a product by marking it as deleted.",
    responses={
        200: {"description": "Product deleted successfully"},
        404: {"model": ErrorResponse, "description": "Product not found"},
        410: {"model": ErrorResponse, "description": "Product already deleted"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def delete_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    """
    Soft delete a product.
    
    - **product_id**: UUID of the product to delete
    
    The product will be marked as deleted with a timestamp but not removed from the database.
    """
    try:
        product = await service.delete_product(product_id)
        return ProductResponse(**product.to_dict())
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductAlreadyDeletedException as e:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )
