# Products REST API

A production-ready REST API for managing products in an e-commerce system. Built with FastAPI, MongoDB, and modern Python best practices.

## 🚀 Features

- **Complete CRUD Operations**: Create, Read, Update, and Delete products
- **Soft Delete**: Products are marked as deleted rather than permanently removed
- **Data Validation**: Comprehensive input validation using Pydantic
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Clean Architecture**: Repository pattern, service layer, and proper separation of concerns
- **Comprehensive Testing**: Unit tests, integration tests, and E2E tests
- **Production Ready**: Error handling, logging, and CORS support

## 📋 Requirements

- Python 3.12+
- MongoDB (local installation)
- UV package manager

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (with Motor async driver)
- **Validation**: Pydantic v2
- **Package Manager**: UV
- **Testing**: Pytest, Playwright
- **Runtime**: Python 3.12

## 📦 Installation

### 1. Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

### 2. Install MongoDB

```bash
# macOS
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community
```

### 3. Clone and Setup Project

```bash
cd products-rest-api

# Install dependencies
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

### 4. Configure Environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env if needed (default settings work for local MongoDB)
```

## 🚀 Running the Application

### Development Server

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:

- **API Base**: http://localhost:8000/api/v1
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Products

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| POST   | `/api/v1/products`      | Create a new product    |
| GET    | `/api/v1/products`      | Get all active products |
| GET    | `/api/v1/products/{id}` | Get product by ID       |
| PUT    | `/api/v1/products/{id}` | Update a product        |
| DELETE | `/api/v1/products/{id}` | Soft delete a product   |

### Product Data Model

```json
{
  "id": "uuid",
  "name": "string (required)",
  "description": "string (optional)",
  "category": "string (required)",
  "price": "number (required, > 0)",
  "stock": "integer (required, >= 0)",
  "createdAt": "datetime",
  "updatedAt": "datetime",
  "deletedAt": "datetime | null"
}
```

## 📖 API Usage Examples

### Create a Product

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "category": "Electronics",
    "price": 29.99,
    "stock": 150
  }'
```

### Get All Products

```bash
curl "http://localhost:8000/api/v1/products"
```

### Get Product by ID

```bash
curl "http://localhost:8000/api/v1/products/{product-id}"
```

### Update a Product

```bash
curl -X PUT "http://localhost:8000/api/v1/products/{product-id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse Pro",
    "price": 34.99,
    "stock": 200
  }'
```

### Delete a Product (Soft Delete)

```bash
curl -X DELETE "http://localhost:8000/api/v1/products/{product-id}"
```

## 🧪 Testing

### Run All Tests

```bash
uv run pytest
```

### Run Unit Tests Only

```bash
uv run pytest -m unit
```

### Run Integration Tests Only

```bash
uv run pytest -m integration
```

### Run E2E Tests Only

**Note**: The API server must be running for E2E tests.

```bash
# Terminal 1: Start the server
uv run uvicorn app.main:app --reload

# Terminal 2: Install Playwright browsers (first time only)
uv run playwright install

# Terminal 2: Run E2E tests
uv run pytest -m e2e
```

### Run Tests with Coverage

```bash
uv run pytest --cov=app --cov-report=html
```

## 📁 Project Structure

```
products-rest-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── database.py             # MongoDB connection
│   ├── models/                 # Domain models
│   │   └── product.py
│   ├── schemas/                # Pydantic schemas
│   │   └── product.py
│   ├── repositories/           # Data access layer
│   │   └── product_repository.py
│   ├── services/               # Business logic layer
│   │   └── product_service.py
│   ├── routers/                # API endpoints
│   │   └── products.py
│   └── exceptions/             # Custom exceptions
│       └── product_exceptions.py
├── tests/
│   ├── conftest.py             # Test fixtures
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── implementations/            # Implementation documentation
│   └── IMPLEMENTATION.md
├── .env                        # Environment variables
├── .env.example                # Environment template
├── .gitignore
├── pyproject.toml              # Project configuration
└── README.md
```

## 🏗️ Architecture

The application follows Clean Architecture principles:

1. **Models Layer**: Domain entities representing business objects
2. **Repository Layer**: Data access abstraction over MongoDB
3. **Service Layer**: Business logic and orchestration
4. **Router Layer**: HTTP request/response handling
5. **Schemas Layer**: Input validation and serialization

### Design Patterns Used

- **Repository Pattern**: Abstracts data access logic
- **Dependency Injection**: Services inject repositories
- **DTO Pattern**: Pydantic schemas for data transfer
- **Soft Delete Pattern**: Preserves data integrity

## 🔒 Security Features

- **Input Validation**: Comprehensive validation using Pydantic
- **CORS Support**: Configurable CORS policy
- **Error Handling**: Proper HTTP status codes and error messages
- **UUID Identifiers**: Prevents enumeration attacks

## 🌐 Environment Variables

| Variable             | Description            | Default                                       |
| -------------------- | ---------------------- | --------------------------------------------- |
| `MONGODB_URL`        | MongoDB connection URL | `mongodb://localhost:27017`                   |
| `MONGODB_DATABASE`   | Database name          | `products_db`                                 |
| `MONGODB_COLLECTION` | Collection name        | `products`                                    |
| `API_V1_PREFIX`      | API version prefix     | `/api/v1`                                     |
| `CORS_ORIGINS`       | Allowed CORS origins   | `http://localhost:3000,http://localhost:8000` |
| `DEBUG`              | Debug mode             | `True`                                        |
| `HOST`               | Server host            | `0.0.0.0`                                     |
| `PORT`               | Server port            | `8000`                                        |

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints throughout
- Document all public APIs
- Write descriptive commit messages

### Adding New Features

1. Create domain model in `app/models/`
2. Define Pydantic schemas in `app/schemas/`
3. Implement repository in `app/repositories/`
4. Add business logic in `app/services/`
5. Create router endpoints in `app/routers/`
6. Write comprehensive tests

### Testing Best Practices

- Write unit tests for services
- Write integration tests for API endpoints
- Write E2E tests for complete workflows
- Aim for >80% code coverage
- Test error scenarios

## 🚀 Deployment

### Using Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv pip install -e .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t products-api .
docker run -p 8000:8000 products-api
```

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use environment-specific MongoDB connection
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Use multiple workers for uvicorn
- [ ] Set up reverse proxy (nginx)
- [ ] Enable HTTPS
- [ ] Implement rate limiting
- [ ] Set up backup strategy for MongoDB

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is created for educational purposes.

## 👥 Authors

Developed as part of Hexaware corporate training program.

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Happy Coding! 🎉**
