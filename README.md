# FAASTAPI

FAASTAPI is a learning project for building a REST API with FastAPI, SQLAlchemy, PostgreSQL, JWT authentication, and Alembic database migrations.

## Features

- User signup and password hashing with bcrypt
- OAuth2 password login with JWT access tokens
- Authenticated post creation, listing, retrieval, editing, and deletion
- User lookup by ID
- PostgreSQL persistence through SQLAlchemy
- Database migration support through Alembic
- Interactive API documentation from FastAPI

## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- PostgreSQL and psycopg2
- Pydantic Settings
- python-jose
- Passlib and bcrypt
- Alembic
- uv for dependency and virtual-environment management

## Prerequisites

- Python 3.12 or newer
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)

## Getting Started

Clone the repository and enter the project directory:

```bash
git clone https://github.com/binaysharma1/API_DEVELOPMENT.git
cd API_DEVELOPMENT
```

Create the project environment and install dependencies:

```bash
uv sync
```

Create a PostgreSQL database, then create a `.env` file in the project root. The following variables are required by the application:

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=db_1
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_URL=postgresql://postgres:your-password@localhost:5432/db_1
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

`DATABASE_URL` is the value used by the application when creating its SQLAlchemy engine. Do not commit `.env`; it is ignored by Git.

## Database Migrations

Apply all available migrations:

```bash
uv run alembic upgrade head
```

Show the applied revision:

```bash
uv run alembic current
```

Create a new migration after changing the SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "describe the change"
uv run alembic upgrade head
```

Roll back the latest migration:

```bash
uv run alembic downgrade -1
```

Use `uv run alembic ...` unless the project virtual environment has been activated with `source .venv/bin/activate`.

## Run the API

Start the development server with:

```bash
uv run fastapi dev app/main.py
```

The API is available at <http://127.0.0.1:8000>.

Interactive documentation is available at:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI schema: <http://127.0.0.1:8000/openapi.json>

## API Endpoints

All versioned routes use the `/api/v1` prefix.

### Authentication

| Method | Path | Description | Authentication |
| --- | --- | --- | --- |
| `POST` | `/api/v1/auth/signup` | Create a user account | No |
| `POST` | `/api/v1/auth/login` | Log in and receive a JWT | No |

The login endpoint uses OAuth2 form fields. Send the user email as `username` and the password as `password`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=user@example.com&password=your-password"
```

Use the returned token for protected requests:

```text
Authorization: Bearer <access-token>
```

### Posts

| Method | Path | Description | Authentication |
| --- | --- | --- | --- |
| `POST` | `/api/v1/posts/create` | Create a post | Bearer token |
| `GET` | `/api/v1/posts/` | List posts | Bearer token |
| `GET` | `/api/v1/posts/{id}` | Get one post | Bearer token |
| `PUT` | `/api/v1/posts/{id}` | Update an owned post | Bearer token |
| `DELETE` | `/api/v1/posts/{id}` | Delete an owned post | Bearer token |

The list endpoint supports these query parameters:

- `limit`: maximum number of posts to return; defaults to `10`
- `skip`: number of posts to skip; defaults to `0`
- `search`: filters posts by title substring

### Users

| Method | Path | Description | Authentication |
| --- | --- | --- | --- |
| `GET` | `/api/v1/user/{id}` | Get a user by ID | No |

### Health Check

| Method | Path | Response |
| --- | --- | --- |
| `GET` | `/` | `{ "message": "Hello World" }` |

## Project Structure

```text
app/
├── main.py              # FastAPI application and router registration
├── config.py            # Environment-based settings
├── database.py          # SQLAlchemy engine, session, and Base
├── models.py            # User and Post database models
├── oauth2.py            # JWT creation and authentication dependency
├── schemas.py            # Pydantic request and response schemas
├── utils.py              # Password hashing and verification
└── routers/
    ├── Auth.py           # Signup and login endpoints
    ├── post.py           # Post endpoints
    └── user.py           # User endpoints
alembic/
├── env.py               # Alembic environment configuration
└── versions/            # Database migration scripts
pyproject.toml           # Project metadata and dependencies
uv.lock                 # Locked dependency versions
```

## Development Notes

- The application currently calls `Base.metadata.create_all()` during startup. Alembic should still be used to manage schema changes in development and production.
- The API currently has no automated test suite.
- Alembic commands must be run from the repository root.
- The current `alembic.ini` contains a database URL for Alembic's online migration path. Keep it aligned with the database configured in `.env` before running migrations against another environment.

## License

No license has been specified for this project yet.
