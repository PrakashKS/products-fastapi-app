"""
FastAPI application main module.
Configures and initializes the FastAPI application.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import db
from app.routers import products


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan context manager.
    Handles startup and shutdown events.
    """
    # Startup: Connect to database
    await db.connect_db()
    yield
    # Shutdown: Close database connection
    await db.close_db()


# Initialize FastAPI application
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    ## Products REST API
    
    A production-ready REST API for managing products in an e-commerce system.
    
    ### Features
    
    * **Create Product**: Add new products to the catalog
    * **List Products**: Get all active products (excludes deleted items)
    * **Get Product**: Retrieve detailed information about a specific product
    * **Update Product**: Modify existing product information
    * **Delete Product**: Soft delete products (preserves data)
    
    ### Data Model
    
    Products include the following fields:
    - **id**: Unique identifier (UUID)
    - **name**: Product name (required)
    - **description**: Product description (optional)
    - **category**: Product category (required)
    - **price**: Product price (required, must be positive)
    - **stock**: Available stock quantity (required, must be non-negative)
    - **createdAt**: Creation timestamp
    - **updatedAt**: Last update timestamp
    - **deletedAt**: Soft delete timestamp (null if active)
    
    ### Technical Stack
    
    - **Framework**: FastAPI
    - **Database**: MongoDB
    - **Runtime**: Python 3.12
    - **Package Manager**: UV
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"] if settings.cors_allow_methods == "*" else settings.cors_allow_methods.split(","),
    allow_headers=["*"] if settings.cors_allow_headers == "*" else settings.cors_allow_headers.split(","),
)

# Include routers
app.include_router(products.router, prefix=settings.api_v1_prefix)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API status.
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing API information.
    """
    return {
        "message": "Welcome to Products REST API",
        "version": settings.app_version,
        "docs": "/docs",
        "api": settings.api_v1_prefix,
    }
