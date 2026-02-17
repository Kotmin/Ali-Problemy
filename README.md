# Ali-Problemy

REST API for managing pet ownership records — who has which animal, and since when.

Built with FastAPI, SQLAlchemy, Pydantic v2, and SQLite.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Running

```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

Interactive API docs available at `http://127.0.0.1:8000/docs`.

## API Endpoints

All endpoints are under `/api/v1/`.

| Method | Route | Description |
|--------|-------|-------------|
| `POST` | `/records` | Create a new ownership record |
| `GET` | `/records` | List all records (paginated, filterable) |
| `GET` | `/records/{id}` | Get a specific record |
| `PUT` | `/records/{id}` | Update a record |
| `DELETE` | `/records/{id}` | Delete a record |
| `GET` | `/health` | Health check |

### Query parameters for `GET /records`

| Param | Default | Description |
|-------|---------|-------------|
| `skip` | `0` | Pagination offset |
| `limit` | `20` | Page size (max 100) |
| `owner_name` | — | Filter by owner name (case-insensitive partial match) |

### Example

```bash
# Create a record
curl -X POST http://127.0.0.1:8000/api/v1/records \
  -H "Content-Type: application/json" \
  -d '{"owner_name": "Ala", "animal_name": "kot", "since_date": "2024-10-31"}'

# List all records
curl http://127.0.0.1:8000/api/v1/records

# Get record by ID
curl http://127.0.0.1:8000/api/v1/records/1

# Update a record
curl -X PUT http://127.0.0.1:8000/api/v1/records/1 \
  -H "Content-Type: application/json" \
  -d '{"animal_name": "pies"}'

# Delete a record
curl -X DELETE http://127.0.0.1:8000/api/v1/records/1
```

## Configuration

Environment variables (or `.env` file):

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_DATABASE_URL` | `sqlite:///./ownership.db` | Database connection string |
| `APP_RATE_LIMIT_WRITE` | `10/minute` | Rate limit for write endpoints |
| `APP_RATE_LIMIT_READ` | `30/minute` | Rate limit for read endpoints |

## Testing

```bash
PYTHONPATH=. pytest tests/ -v
```

## Project Structure

```
app/
  main.py            # FastAPI app, lifespan, middleware
  config.py          # Settings via pydantic-settings
  database.py        # SQLAlchemy engine, session, get_db
  models.py          # OwnershipRecord ORM model
  schemas.py         # Pydantic request/response schemas
  rate_limiter.py    # slowapi rate limiter
  routers/
    ownership.py     # CRUD endpoints
tests/
  conftest.py        # Fixtures (in-memory SQLite, TestClient)
  test_ownership_crud.py
  test_validation.py
  test_models.py
  test_rate_limiter.py
```
