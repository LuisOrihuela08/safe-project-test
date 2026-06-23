# Safe Inventory API

A minimal FastAPI REST API for inventory management using in-memory storage.
Built with clean code practices and no hardcoded secrets.

## Stack

- **Python 3.11+**
- **FastAPI** — web framework
- **Pydantic v2** — data validation
- **pydantic-settings** — environment-based config
- **pytest** — testing

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs available at: http://localhost:8000/docs

## Tests

```bash
pytest
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /items/ | List active items |
| GET | /items/{id} | Get item by ID |
| POST | /items/ | Create item |
| PUT | /items/{id} | Update item |
| DELETE | /items/{id} | Delete item |
