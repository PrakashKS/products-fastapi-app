"""
Product Pydantic schemas for request/response validation.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ProductCreate(BaseModel):
    """Schema for creating a new product."""

    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    description: Optional[str] = Field(
        None, max_length=1000, description="Product description"
    )
    category: str = Field(
        ..., min_length=1, max_length=100, description="Product category"
    )
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    stock: int = Field(..., ge=0, description="Stock quantity (must be non-negative)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Wireless Mouse",
                    "description": "Ergonomic wireless mouse with USB receiver",
                    "category": "Electronics",
                    "price": 29.99,
                    "stock": 150,
                }
            ]
        }
    }


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Product name"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Product description"
    )
    category: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Product category"
    )
    price: Optional[float] = Field(
        None, gt=0, description="Product price (must be positive)"
    )
    stock: Optional[int] = Field(
        None, ge=0, description="Stock quantity (must be non-negative)"
    )

    @field_validator("name", "category", "description")
    @classmethod
    def validate_non_empty_strings(cls, v: Optional[str]) -> Optional[str]:
        """Ensure strings are not empty or whitespace only."""
        if v is not None and not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Wireless Mouse Pro",
                    "price": 34.99,
                    "stock": 200,
                }
            ]
        }
    }


class ProductResponse(BaseModel):
    """Schema for product response."""

    id: UUID = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price")
    stock: int = Field(..., description="Stock quantity")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")
    deletedAt: Optional[datetime] = Field(None, description="Deletion timestamp")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Wireless Mouse",
                    "description": "Ergonomic wireless mouse with USB receiver",
                    "category": "Electronics",
                    "price": 29.99,
                    "stock": 150,
                    "createdAt": "2026-02-06T10:30:00",
                    "updatedAt": "2026-02-06T10:30:00",
                    "deletedAt": None,
                }
            ]
        }
    }


class ProductListResponse(BaseModel):
    """Schema for list of products response."""

    products: list[ProductResponse] = Field(..., description="List of products")
    total: int = Field(..., description="Total number of products")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "products": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "name": "Wireless Mouse",
                            "description": "Ergonomic wireless mouse",
                            "category": "Electronics",
                            "price": 29.99,
                            "stock": 150,
                            "createdAt": "2026-02-06T10:30:00",
                            "updatedAt": "2026-02-06T10:30:00",
                            "deletedAt": None,
                        }
                    ],
                    "total": 1,
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str = Field(..., description="Error message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": "Product not found",
                }
            ]
        }
    }
