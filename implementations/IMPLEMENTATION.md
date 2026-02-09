# Implementation Documentation

## Project Overview

This document provides detailed implementation notes for the Products REST API application.

**Project Name**: Products REST API  
**Technology**: FastAPI, MongoDB, Python 3.12  
**Architecture**: Clean Architecture with Repository Pattern  
**Created**: February 6, 2026

---

## 📋 Requirements Analysis

### Functional Requirements

1. **Create Product**: Add new products with validation
2. **List Products**: Retrieve all active (non-deleted) products
3. **Get Product**: Retrieve specific product details by UUID
4. **Update Product**: Modify existing product information
5. **Delete Product**: Soft delete products (preserve data)

### Non-Functional Requirements

1. **Performance**: Async operations for better scalability
2. **Maintainability**: Clean architecture, separation of concerns
3. **Testability**: Comprehensive test coverage (unit, integration, E2E)
4. **Documentation**: Auto-generated Swagger/OpenAPI docs
5. **Data Integrity**: Soft deletes, UUID identifiers
6. **Validation**: Strong input validation using Pydantic

---

## 🏗️ Architecture Design

### Layered Architecture

The application follows a clean, layered architecture:

```
┌─────────────────────────────────────┐
│         Router Layer                │  ← HTTP Request/Response
│      (API Endpoints)                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Service Layer                │  ← Business Logic
│      (Product Service)               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Repository Layer               │  ← Data Access
│    (Product Repository)              │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│          Database                    │  ← MongoDB
│         (Motor)                      │
└──────────────────────────────────────┘
```

### Layer Responsibilities

1. **Router Layer** (`app/routers/`)
   - Handle HTTP requests/responses
   - Route configuration
   - Request/response serialization
   - HTTP status code management
   - Error handling and exception mapping

2. **Service Layer** (`app/services/`)
   - Business logic implementation
   - Validation of business rules
   - Orchestration between repositories
   - Transaction management
   - Domain-specific operations

3. **Repository Layer** (`app/repositories/`)
   - Data access abstraction
   - CRUD operations
   - Query composition
   - Database-specific logic
   - Data mapping (DB ↔ Domain models)

4. **Models Layer** (`app/models/`)
   - Domain entities
   - Business object representation
   - Domain logic (soft delete, update)

5. **Schemas Layer** (`app/schemas/`)
   - Request/Response DTOs
   - Input validation rules
   - Serialization/Deserialization

---

## 💾 Database Design

### MongoDB Collection Structure

**Collection Name**: `products`

**Document Schema**:

```json
{
  "_id": ObjectId,              // MongoDB internal ID
  "id": "UUID string",          // Application-level unique ID
  "name": "string",             // Product name (required)
  "description": "string|null", // Product description (optional)
  "category": "string",         // Product category (required)
  "price": number,              // Price (must be > 0)
  "stock": number,              // Stock quantity (must be >= 0)
  "createdAt": "ISO datetime",  // Creation timestamp
  "updatedAt": "ISO datetime",  // Last update timestamp
  "deletedAt": "ISO datetime|null" // Soft delete timestamp
}
```

### Indexes

1. **Unique Index on `id`**: Ensures UUID uniqueness
2. **Index on `category`**: Improves filtering performance
3. **Index on `deletedAt`**: Optimizes queries for active products

```python
await collection.create_index("id", unique=True)
await collection.create_index("category")
await collection.create_index("deletedAt")
```

---

## 🔧 Implementation Details

### 1. Configuration Management

**File**: `app/config.py`

**Implementation**:

- Uses `pydantic-settings` for type-safe configuration
- Loads from `.env` file automatically
- Provides default values for all settings
- Cached using `@lru_cache` for performance

**Key Features**:

- Environment variable validation
- Type conversion
- CORS origins parsing

### 2. Database Connection

**File**: `app/database.py`

**Implementation**:

- Singleton pattern for database connection
- Async Motor client for MongoDB
- Lifespan management (connect on startup, close on shutdown)
- Automatic index creation

**Connection Flow**:

```python
1. App startup → connect_db()
2. Create Motor client
3. Select database and collection
4. Create indexes
5. App shutdown → close_db()
```

### 3. Domain Model

**File**: `app/models/product.py`

**Implementation**:

- Pure Python class (no ORM)
- UUID-based identification
- Soft delete logic
- Update method for partial updates
- Serialization methods (to_dict, from_dict)

**Design Decisions**:

- UUID instead of MongoDB ObjectId (prevents enumeration, portable)
- Soft delete preserves audit trail
- Separate createdAt/updatedAt for tracking

### 4. Pydantic Schemas

**File**: `app/schemas/product.py`

**Schemas**:

1. **ProductCreate**: For creating new products
   - All required fields except description
   - Validation: price > 0, stock >= 0

2. **ProductUpdate**: For updating products
   - All fields optional (partial update)
   - Same validation rules apply

3. **ProductResponse**: For API responses
   - Includes all fields including timestamps
   - UUID serialization

4. **ProductListResponse**: For list endpoints
   - Array of products + total count

5. **ErrorResponse**: Standardized error format

**Validation Rules**:

- `name`: 1-200 characters, required
- `description`: max 1000 characters, optional
- `category`: 1-100 characters, required
- `price`: positive float, required
- `stock`: non-negative integer, required

### 5. Repository Pattern

**File**: `app/repositories/product_repository.py`

**Methods**:

- `create(product)`: Insert new product
- `find_by_id(id)`: Get product by UUID
- `find_all(include_deleted)`: List products
- `update(product)`: Update existing product
- `delete(id)`: Hard delete (rarely used)
- `exists(id)`: Check existence

**Error Handling**:

- Wraps all database exceptions in `DatabaseException`
- Provides meaningful error messages
- Ensures consistent error handling

### 6. Service Layer

**File**: `app/services/product_service.py`

**Business Logic**:

- Validates product exists before operations
- Checks soft-delete status
- Prevents operations on deleted products
- Partial update support

**Error Scenarios**:

- Product not found → `ProductNotFoundException`
- Product deleted → `ProductAlreadyDeletedException`
- Validation failure → `ProductValidationException`

### 7. API Endpoints

**File**: `app/routers/products.py`

**Endpoints**:

1. **POST /api/v1/products** (Create)
   - Status: 201 Created
   - Returns: ProductResponse
   - Errors: 400 (validation), 500 (server)

2. **GET /api/v1/products** (List)
   - Status: 200 OK
   - Returns: ProductListResponse
   - Filters out deleted products

3. **GET /api/v1/products/{id}** (Get)
   - Status: 200 OK
   - Returns: ProductResponse
   - Errors: 404 (not found), 410 (deleted)

4. **PUT /api/v1/products/{id}** (Update)
   - Status: 200 OK
   - Returns: ProductResponse
   - Supports partial updates
   - Errors: 404, 410, 400, 500

5. **DELETE /api/v1/products/{id}** (Soft Delete)
   - Status: 200 OK
   - Returns: ProductResponse (with deletedAt)
   - Errors: 404, 410, 500

**HTTP Status Codes**:

- `200 OK`: Successful operation
- `201 Created`: Product created
- `400 Bad Request`: Validation error
- `404 Not Found`: Product doesn't exist
- `410 Gone`: Product soft-deleted
- `422 Unprocessable Entity`: Pydantic validation error
- `500 Internal Server Error`: Server error

### 8. Exception Handling

**File**: `app/exceptions/product_exceptions.py`

**Custom Exceptions**:

1. `ProductNotFoundException`: Product doesn't exist
2. `ProductAlreadyDeletedException`: Product is soft-deleted
3. `ProductValidationException`: Business rule violation
4. `DatabaseException`: Database operation failure

**Exception Mapping**:

- Router layer catches exceptions
- Maps to appropriate HTTP status codes
- Returns consistent error response format

### 9. CORS Configuration

**File**: `app/main.py`

**Implementation**:

- Configurable via environment variables
- Supports multiple origins
- Allows credentials
- Configurable methods and headers

**Security Considerations**:

- Don't use `*` in production
- Specify exact origins
- Limit allowed methods

---

## 🧪 Testing Strategy

### Test Pyramid

```
        ┌────────────┐
        │    E2E     │  ← Playwright (full workflows)
        │   Tests    │
    ┌───┴────────────┴───┐
    │   Integration      │  ← Pytest + httpx (API tests)
    │      Tests          │
┌───┴──────────────────────┴───┐
│      Unit Tests              │  ← Pytest + mocks (service logic)
└──────────────────────────────┘
```

### 1. Unit Tests

**File**: `tests/unit/test_product_service.py`

**Purpose**: Test business logic in isolation

**Approach**:

- Mock repository layer
- Test all service methods
- Test error scenarios
- Verify method calls

**Coverage**:

- Product creation
- Retrieval (found/not found/deleted)
- List all products
- Update (partial/full)
- Soft delete
- Error handling

### 2. Integration Tests

**File**: `tests/integration/test_product_api.py`

**Purpose**: Test complete API flow with test database

**Approach**:

- Real database (separate test database)
- HTTP client (httpx)
- Test all endpoints
- Verify database state

**Coverage**:

- All CRUD operations
- Validation errors
- Soft delete behavior
- List filtering (excludes deleted)
- HTTP status codes

### 3. E2E Tests

**File**: `tests/e2e/test_product_e2e.py`

**Purpose**: Test complete user workflows

**Approach**:

- Playwright API testing
- Real server (must be running)
- Multi-step scenarios

**Scenarios**:

- Complete product lifecycle
- Multiple products management
- Error handling workflow
- API documentation access

### Test Fixtures

**File**: `tests/conftest.py`

**Fixtures**:

1. `event_loop`: Async test support
2. `test_db`: Test database setup/teardown
3. `client`: HTTP test client
4. `sample_product_data`: Test data

---

## 🔐 Security Considerations

### 1. Input Validation

- Pydantic validates all inputs
- Length restrictions on strings
- Range validation on numbers
- Type safety

### 2. Data Integrity

- UUID prevents enumeration attacks
- Soft delete preserves audit trail
- Timestamps track changes

### 3. Error Messages

- Don't leak sensitive information
- Generic error messages externally
- Detailed logs internally

### 4. CORS

- Configured for specific origins
- No wildcard in production
- Credentials support optional

### 5. Database

- Indexed queries for performance
- No SQL injection (NoSQL database)
- Connection pooling via Motor

---

## 🚀 Performance Optimizations

### 1. Async Operations

- All I/O operations are async
- Motor async driver for MongoDB
- FastAPI async endpoints

### 2. Database Indexes

- Unique index on `id`
- Index on `category`
- Index on `deletedAt`

### 3. Connection Pooling

- Motor manages connection pool
- Reuses connections
- Configurable pool size

### 4. Caching

- Settings cached with `@lru_cache`
- Singleton database connection

---

## 📊 Monitoring and Observability

### Health Check Endpoint

**Endpoint**: `GET /health`

**Response**:

```json
{
  "status": "healthy",
  "service": "Products REST API",
  "version": "1.0.0"
}
```

### Logging

- Print statements for startup/shutdown
- Exception logging in handlers
- Can be extended with proper logging framework

### Future Enhancements

1. Structured logging (JSON logs)
2. Request ID tracking
3. Performance metrics
4. Error rate monitoring
5. Database query metrics

---

## 🔄 Deployment Considerations

### Environment Setup

1. **Development**
   - Local MongoDB
   - Debug mode enabled
   - CORS allows localhost

2. **Staging**
   - Shared MongoDB instance
   - Debug mode enabled
   - Limited CORS

3. **Production**
   - MongoDB cluster/replica set
   - Debug mode disabled
   - Strict CORS policy
   - Multiple workers
   - Reverse proxy (nginx)
   - HTTPS enabled

### Scaling

1. **Horizontal Scaling**
   - Multiple uvicorn workers
   - Load balancer
   - Stateless application

2. **Database Scaling**
   - MongoDB replica set
   - Read replicas
   - Sharding (if needed)

### CI/CD Pipeline

Recommended steps:

1. Lint code (ruff, black)
2. Type check (mypy)
3. Run unit tests
4. Run integration tests
5. Build Docker image
6. Deploy to staging
7. Run E2E tests
8. Deploy to production

---

## 📝 Future Enhancements

### Potential Features

1. **Authentication & Authorization**
   - JWT tokens
   - Role-based access control
   - API keys

2. **Pagination**
   - Cursor-based pagination
   - Page size limits
   - Sorting options

3. **Filtering & Search**
   - Filter by category
   - Price range filters
   - Text search
   - MongoDB aggregation

4. **Rate Limiting**
   - Per-user rate limits
   - Redis-based limiter
   - Throttling

5. **Caching**
   - Redis cache for frequently accessed products
   - Cache invalidation on updates
   - TTL configuration

6. **File Uploads**
   - Product images
   - S3/cloud storage
   - Image optimization

7. **Webhooks**
   - Notify on product updates
   - Async event processing
   - Retry logic

8. **Analytics**
   - Product view tracking
   - Inventory alerts
   - Sales reporting

9. **API Versioning**
   - Multiple API versions
   - Deprecation strategy
   - Version negotiation

10. **GraphQL**
    - GraphQL endpoint
    - Flexible queries
    - Type system

---

## 🐛 Common Issues and Solutions

### Issue 1: MongoDB Connection Failed

**Symptom**: App fails to start with connection error

**Solution**:

- Ensure MongoDB is running: `brew services start mongodb-community`
- Check `MONGODB_URL` in `.env`
- Verify network connectivity

### Issue 2: Import Errors

**Symptom**: Module not found errors

**Solution**:

- Install dependencies: `uv pip install -e .`
- Ensure correct Python version: `python --version`
- Check virtual environment activation

### Issue 3: Tests Failing

**Symptom**: Integration tests fail

**Solution**:

- Ensure MongoDB is running
- Check test database is separate
- Clear test database: Manual cleanup

### Issue 4: E2E Tests Fail

**Symptom**: Playwright tests timeout

**Solution**:

- Start the server first
- Install Playwright browsers: `playwright install`
- Check server URL in tests

---

## 📚 References

### Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)

### Best Practices

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [REST API Design](https://restfulapi.net/)

---

## ✅ Implementation Checklist

- [x] Project structure created
- [x] Configuration management implemented
- [x] Database connection setup
- [x] Domain models defined
- [x] Pydantic schemas created
- [x] Repository layer implemented
- [x] Service layer implemented
- [x] API routers created
- [x] Exception handling implemented
- [x] CORS configured
- [x] Health check endpoint
- [x] Unit tests written
- [x] Integration tests written
- [x] E2E tests written
- [x] README documentation
- [x] Implementation documentation
- [x] Swagger documentation auto-generated

---

## 📞 Contact

For questions or issues related to this implementation:

- Create an issue in the repository
- Contact the development team

---

**Last Updated**: February 6, 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
