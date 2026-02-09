# Quick Start Guide

## Prerequisites Checklist

- [ ] Python 3.12 or higher installed
- [ ] MongoDB installed and running
- [ ] UV package manager installed

## Installation Steps

### 1. Install MongoDB (if not already installed)

**macOS:**

```bash
brew install mongodb-community
brew services start mongodb-community
```

### 2. Install UV Package Manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or using pip:

```bash
pip install uv
```

### 3. Install Project Dependencies

```bash
cd products-rest-api
uv pip install -e .
uv pip install -e ".[dev]"
```

## Running the Application

### Option 1: Using the start script (easiest)

```bash
chmod +x start.sh
./start.sh
```

### Option 2: Using Make

```bash
make install  # First time only
make run
```

### Option 3: Manual command

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Accessing the API

Once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **API Endpoints**: http://localhost:8000/api/v1/products
- **Health Check**: http://localhost:8000/health

## Testing the API

### Using Swagger UI (Recommended for beginners)

1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"

### Using cURL

**Create a product:**

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

**Get all products:**

```bash
curl "http://localhost:8000/api/v1/products"
```

## Running Tests

**All tests:**

```bash
make test
```

**Unit tests only:**

```bash
make test-unit
```

**Integration tests:**

```bash
make test-integration
```

**E2E tests (requires server to be running):**

```bash
# Terminal 1: Start server
make run

# Terminal 2: Run E2E tests
uv run playwright install  # First time only
make test-e2e
```

## Stopping the Application

Press `Ctrl+C` in the terminal where the server is running.

## Troubleshooting

**MongoDB connection error:**

- Ensure MongoDB is running: `brew services list`
- Start MongoDB: `brew services start mongodb-community`

**Import errors:**

- Reinstall dependencies: `make install`

**Port already in use:**

- Change port in `.env` file
- Or kill the process using port 8000: `lsof -ti:8000 | xargs kill`

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [implementations/IMPLEMENTATION.md](implementations/IMPLEMENTATION.md) for architecture details
3. Explore the API using Swagger UI
4. Try creating, updating, and deleting products
5. Review the test files in `tests/` for examples

## Support

For issues, refer to:

- [README.md](README.md) - Comprehensive documentation
- [implementations/IMPLEMENTATION.md](implementations/IMPLEMENTATION.md) - Technical details
- API docs at http://localhost:8000/docs
