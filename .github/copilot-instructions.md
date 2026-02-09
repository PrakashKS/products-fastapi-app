# Products REST API - Copilot Instructions

## 📋 Project Overview

A production-ready REST API for managing products in an e-commerce system. Built with FastAPI, MongoDB, and modern Python best practices following clean architecture principles.

### Key Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete products
- **Soft Delete Pattern**: Products are marked as deleted rather than permanently removed for data integrity
- **Data Validation**: Comprehensive input validation using Pydantic v2
- **Auto-generated API Documentation**: Swagger/OpenAPI docs at `/docs` and ReDoc at `/redoc`
- **Clean Architecture**: Repository pattern, service layer, and proper separation of concerns
- **Comprehensive Testing Suite**: Unit tests, integration tests, and E2E tests with Playwright
- **Production Ready**: Error handling, logging, CORS support, and database indexing

## 🏗️ Architecture

The application follows **Clean Architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│                    Presentation Layer               │
│              (FastAPI Routers/Controllers)          │
│                  app/routers/*.py                   │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                  Application Layer                   │
│                (Business Logic/Services)             │
│                 app/services/*.py                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│                   Domain Layer                       │
│              (Domain Models/Entities)                │
│                  app/models/*.py                     │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              Infrastructure Layer                    │
│            (Database/Repository Pattern)             │
│            app/repositories/*.py                     │
│               app/database.py                        │
└─────────────────────────────────────────────────────┘
```

### Layer Responsibilities

#### 1. **Presentation Layer** (`app/routers/`)

- HTTP request/response handling
- Route definitions and API endpoints
- Request validation using Pydantic schemas
- HTTP status code management
- Exception to HTTP error mapping
- Dependency injection setup

#### 2. **Application Layer** (`app/services/`)

- Business logic orchestration
- Transaction coordination
- Business rule validation
- Coordination between repositories
- Use case implementations

#### 3. **Domain Layer** (`app/models/`)

- Core business entities (Product model)
- Domain logic (soft delete, update operations)
- Pure Python objects, framework-agnostic
- Business invariants and rules

#### 4. **Infrastructure Layer** (`app/repositories/`, `app/database.py`)

- Database connections and configuration
- Data persistence operations
- Query implementations
- External service integrations
- MongoDB Motor async driver usage

### Additional Components

- **Schemas** (`app/schemas/`): Pydantic models for request/response validation and serialization
- **Exceptions** (`app/exceptions/`): Custom exception classes for domain-specific errors
- **Configuration** (`app/config.py`): Environment-based settings using Pydantic Settings

## 🛠️ Tech Stack

### Core Framework & Runtime

- **Python**: 3.12+
- **FastAPI**: 0.115.0+ - Modern, high-performance web framework
- **Uvicorn**: 0.30.0+ - ASGI server with auto-reload for development

### Database

- **MongoDB**: NoSQL document database
- **Motor**: 3.6.0+ - Async Python driver for MongoDB

### Data Validation & Configuration

- **Pydantic**: 2.9.0+ - Data validation using Python type annotations
- **Pydantic Settings**: 2.5.0+ - Settings management from environment variables
- **python-dotenv**: 1.0.0+ - Environment variable loading from .env files

### Testing

- **pytest**: 8.3.0+ - Testing framework
- **pytest-asyncio**: 0.24.0+ - Async test support
- **httpx**: 0.27.0+ - HTTP client for integration tests
- **Playwright**: 1.48.0+ - E2E browser automation testing
- **pytest-playwright**: 0.5.0+ - Pytest plugin for Playwright

### Package Management

- **UV**: Modern, fast Python package manager

## 🌐 API Endpoints

### Base URL

```
http://localhost:8000/api/v1
```

### Health Check

```http
GET /health
```

**Description**: Verify API status and get service information

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "service": "Products REST API",
  "version": "1.0.0"
}
```

---

### 1. Create Product

```http
POST /api/v1/products
```

**Description**: Create a new product in the catalog

**Request Body**:

```json
{
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "category": "Electronics",
  "price": 29.99,
  "stock": 150
}
```

**Validation Rules**:

- `name`: Required, 1-200 characters
- `description`: Optional, max 1000 characters
- `category`: Required, 1-100 characters
- `price`: Required, must be positive (> 0)
- `stock`: Required, must be non-negative (≥ 0)

**Response**: `201 Created`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse with USB receiver",
  "category": "Electronics",
  "price": 29.99,
  "stock": 150,
  "createdAt": "2026-02-09T10:30:00.000Z",
  "updatedAt": "2026-02-09T10:30:00.000Z",
  "deletedAt": null
}
```

**Error Responses**:

- `400 Bad Request`: Invalid input data
- `500 Internal Server Error`: Database error

---

### 2. Get All Products

```http
GET /api/v1/products
```

**Description**: Retrieve all active (non-deleted) products

**Response**: `200 OK`

```json
{
  "products": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Wireless Mouse",
      "description": "Ergonomic wireless mouse",
      "category": "Electronics",
      "price": 29.99,
      "stock": 150,
      "createdAt": "2026-02-09T10:30:00.000Z",
      "updatedAt": "2026-02-09T10:30:00.000Z",
      "deletedAt": null
    }
  ],
  "total": 1
}
```

**Error Responses**:

- `500 Internal Server Error`: Database error

---

### 3. Get Product by ID

```http
GET /api/v1/products/{product_id}
```

**Description**: Retrieve a specific product by its UUID

**Path Parameters**:

- `product_id`: UUID of the product

**Response**: `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Wireless Mouse",
  "description": "Ergonomic wireless mouse",
  "category": "Electronics",
  "price": 29.99,
  "stock": 150,
  "createdAt": "2026-02-09T10:30:00.000Z",
  "updatedAt": "2026-02-09T10:30:00.000Z",
  "deletedAt": null
}
```

**Error Responses**:

- `404 Not Found`: Product does not exist
- `410 Gone`: Product has been soft-deleted
- `500 Internal Server Error`: Database error

---

### 4. Update Product

```http
PUT /api/v1/products/{product_id}
```

**Description**: Update an existing product's information

**Path Parameters**:

- `product_id`: UUID of the product

**Request Body** (all fields optional):

```json
{
  "name": "Wireless Mouse Pro",
  "description": "Updated description",
  "category": "Electronics",
  "price": 34.99,
  "stock": 200
}
```

**Validation Rules**:

- `name`: Optional, 1-200 characters, not empty/whitespace
- `description`: Optional, max 1000 characters
- `category`: Optional, 1-100 characters, not empty/whitespace
- `price`: Optional, must be positive (> 0)
- `stock`: Optional, must be non-negative (≥ 0)

**Response**: `200 OK`

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Wireless Mouse Pro",
  "description": "Updated description",
  "category": "Electronics",
  "price": 34.99,
  "stock": 200,
  "createdAt": "2026-02-09T10:30:00.000Z",
  "updatedAt": "2026-02-09T11:45:00.000Z",
  "deletedAt": null
}
```

**Error Responses**:

- `400 Bad Request`: Invalid input data
- `404 Not Found`: Product does not exist
- `410 Gone`: Product has been soft-deleted
- `500 Internal Server Error`: Database error

---

### 5. Delete Product (Soft Delete)

```http
DELETE /api/v1/products/{product_id}
```

**Description**: Soft delete a product (sets `deletedAt` timestamp, preserves data)

**Path Parameters**:

- `product_id`: UUID of the product

**Response**: `204 No Content`

**Error Responses**:

- `404 Not Found`: Product does not exist
- `410 Gone`: Product already deleted
- `500 Internal Server Error`: Database error

---

## 📊 Data Model

### Product Entity

```python
{
  "id": "UUID",              # Unique identifier (auto-generated)
  "name": "string",          # Product name (1-200 chars)
  "description": "string",   # Optional description (max 1000 chars)
  "category": "string",      # Product category (1-100 chars)
  "price": float,            # Price (must be > 0)
  "stock": int,              # Stock quantity (must be ≥ 0)
  "createdAt": "datetime",   # Creation timestamp (UTC)
  "updatedAt": "datetime",   # Last update timestamp (UTC)
  "deletedAt": "datetime"    # Soft delete timestamp (null if active)
}
```

### Database Indexes

- `id`: Unique index for fast lookups
- `category`: Index for category filtering
- `deletedAt`: Index for filtering active/deleted products

## 🚫 Don'ts - Important Guidelines

### Security & Configuration

- ❌ **NEVER access `.env` files directly** - Always use `.env.example` as a reference
- ❌ **NEVER commit `.env` files** to version control
- ❌ **NEVER hardcode credentials** or sensitive data in code
- ❌ **NEVER expose database connection strings** in error messages or logs

### Architecture & Code Quality

- ❌ **NEVER bypass the service layer** - Always route requests through services, not directly to repositories
- ❌ **NEVER put business logic in routers** - Keep routers thin, business logic belongs in services
- ❌ **NEVER put database logic in services** - Database operations should be in repositories only
- ❌ **NEVER use synchronous database calls** - Always use async/await with Motor
- ❌ **NEVER skip input validation** - Always validate using Pydantic schemas
- ❌ **NEVER return raw exceptions to clients** - Use proper exception handling and HTTP status codes

### Data Management

- ❌ **NEVER perform hard deletes** - Always use soft delete pattern (set `deletedAt` timestamp)
- ❌ **NEVER return deleted products in list endpoints** - Filter by `deletedAt: null`
- ❌ **NEVER modify `createdAt` after creation** - This field is immutable
- ❌ **NEVER forget to update `updatedAt`** - Update this timestamp on every modification

### Testing

- ❌ **NEVER skip tests for new features** - Maintain comprehensive test coverage
- ❌ **NEVER test against production database** - Always use test database or mocks
- ❌ **NEVER commit commented-out test code** - Remove or fix broken tests

### API Design

- ❌ **NEVER change existing API contracts** without versioning
- ❌ **NEVER return MongoDB's `_id` field** - Remove it from responses
- ❌ **NEVER use HTTP 200 for errors** - Use appropriate status codes (404, 400, 500, etc.)
- ❌ **NEVER expose stack traces** in production error responses

### Development Practices

- ❌ **NEVER run migrations manually in production** - Use automated migration tools
- ❌ **NEVER deploy without running tests** - CI/CD should run full test suite
- ❌ **NEVER ignore linting warnings** - Maintain code quality standards
- ❌ **NEVER use `print()` for logging** - Use proper logging framework

## 📝 Environment Configuration

**Reference File**: `.env.example`

All configuration should be done through environment variables. Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

### Configuration Categories

#### MongoDB Settings

- `MONGODB_URL`: Database connection string
- `MONGODB_DATABASE`: Database name
- `MONGODB_COLLECTION`: Collection name for products

#### Application Settings

- `APP_NAME`: Application name
- `APP_VERSION`: Current version
- `API_V1_PREFIX`: API version prefix
- `DEBUG`: Debug mode (True/False)

#### CORS Settings

- `CORS_ORIGINS`: Allowed origins (comma-separated)
- `CORS_ALLOW_CREDENTIALS`: Allow credentials
- `CORS_ALLOW_METHODS`: Allowed HTTP methods
- `CORS_ALLOW_HEADERS`: Allowed headers

#### Server Settings

- `HOST`: Server host
- `PORT`: Server port

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── unit/              # Fast, isolated tests for services and models
├── integration/       # Tests with database interactions
└── e2e/              # Full workflow tests with Playwright
```

### Test Commands

```bash
# Run all tests
make test

# Run specific test categories
make test-unit          # Unit tests only
make test-integration   # Integration tests only
make test-e2e          # E2E tests (server must be running)

# Run with coverage
make test-coverage
```

### Test Markers

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.e2e`: End-to-end tests

## 🚀 Quick Start Commands

```bash
# Install dependencies
make install

# Run development server
make run

# Run all tests
make test

# View API documentation
# Open http://localhost:8000/docs (Swagger UI)
# Open http://localhost:8000/redoc (ReDoc)
```

## 📚 Additional Resources

- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`
- **Quick Start Guide**: See `QUICKSTART.md`
- **Detailed README**: See `README.md`

---

**Note**: This is a training project demonstrating FastAPI best practices, clean architecture, and comprehensive testing strategies.
