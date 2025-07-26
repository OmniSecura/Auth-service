# Auth Service

A FastAPI-based microservice providing authentication and authorization APIs.

## Running with Docker

1. Edit the `.env` file to configure database credentials and ports. The sample
   file defines `USERNAME`, `PASSWORD`, `POSTGRES_DB` as well as
   `HOST_API_PORT` and `HOST_DB_PORT` which control the host-side ports used by
   Docker.

2. Build the Docker image and run the container exposing the API port
   (`HOST_API_PORT`, default `18080`):

```bash
docker build -t auth-service .
docker run -p ${HOST_API_PORT}:8000 --env-file .env auth-service
```

The API will be available at `http://localhost:${HOST_API_PORT}`.

## Deploying with Docker Compose

Docker Compose can start the API together with a bundled PostgreSQL instance.
Port mappings are controlled via `HOST_API_PORT` and `HOST_DB_PORT`.
Use the provided `docker-compose.yml`:

```bash
docker compose up --build
```

The service listens on `HOST_API_PORT` (default `18080`), while PostgreSQL is
reachable on `HOST_DB_PORT` (default `35432`). Adjust these values in `.env` if
needed.
Additional services (like a frontend) can be added to the compose file to run
alongside the API and database.