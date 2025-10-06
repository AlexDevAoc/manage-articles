# Manage Articles API

Project for manage articles, with redis, python and postgresql. This API allows creating, reading, updating, and deleting articles, with a caching layer provided by Redis.

## Features

- **FastAPI**: High-performance web framework for building APIs.
- **SQLAlchemy**: ORM for interacting with the PostgreSQL database.
- **Alembic**: Database migration tool for managing schema changes.
- **Redis**: In-memory data store used for caching article data.
- **Docker & Docker Compose**: For containerizing and running the application stack.
- **Poetry**: Dependency management.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

Follow these steps to set up and run the application locally.

### 1. Clone the Repository

```bash
git clone https://github.com/AlexDevAoc/manage-articles.git
cd manage-articles
```

### 2. Create Environment File

Create a `.env` file in the root of the project by copying the example template.

```bash
cp .env.template .env
```

The `.env` file contains the necessary environment variables for the database connection, API key, and Redis. The default values are suitable for the local Docker setup.

```properties
# .env
DATABASE_URL="postgresql://postgres:postgres@db:5432/articles_db"
API_KEY="test"
REDIS_URL="redis://redis:6379/0"
ARTICLE_CACHE_TTL="120"
```

### 3. Build and Run the Application

Use Docker Compose to build the images and start the services (API, database, and Redis).

```bash
docker compose up --build
```

- The `--build` flag ensures that the Docker images are rebuilt if there are any changes in the `Dockerfile` or the source code.
- The services will start in attached mode, so you can see the logs in your terminal. To run them in the background, use `docker compose up -d --build`.

### How it Works

- The `api` service will automatically run database migrations using Alembic upon startup thanks to the `entrypoint.sh` script.
- The FastAPI application will be available on port `8000`.

## Usage

### API Documentation

Once the application is running, you can access the interactive API documentation (Swagger UI) at:

[http://localhost:8000/docs](http://localhost:8000/docs)

From there, you can explore and test all the available endpoints.

### Authentication

All endpoints are protected by an API key. To authorize your requests in the Swagger UI:
1. Click the "Authorize" button.
2. Enter the value of `API_KEY` from your `.env` file (default is `test`) in the `api_key` field.
3. Click "Authorize".

### Stopping the Application

To stop the running services, press `Ctrl+C` in the terminal where `docker compose` is running. If you are running in detached mode, use:

```bash
docker compose down
```

To stop the services and remove the data volumes (database and cache will be cleared), use:
```bash
docker compose down -v
```
