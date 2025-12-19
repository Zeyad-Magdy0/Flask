# Flask Backend with PostgreSQL & Redis (Docker Compose)

This project is a containerized backend application built with Flask, PostgreSQL, and Redis, orchestrated using Docker Compose.

The purpose of this project is to demonstrate real-world backend and DevOps concepts such as multi-container application design, Docker networking, persistent storage, configuration management, and caching strategies.

---

## Architecture Overview

The application consists of three main components:

Backend (Flask + Gunicorn)  
- Exposes a REST API  
- Handles business logic  
- Communicates with PostgreSQL and Redis  

PostgreSQL  
- Relational database  
- Stores application data persistently using Docker volumes  

Redis  
- In-memory cache  
- Implements a cache-aside pattern to improve read performance  

Request flow:
Client → Flask API → Redis (cache) → PostgreSQL (on cache miss) → Redis (cache update) → Client

---

## Project Structure

flask/  
├── docker-compose.yml  
├── README.md  
└── backend/  
    ├── Dockerfile  
    ├── app.py  
    ├── config.py  
    ├── db.py  
    ├── cache.py  
    ├── requirements.txt  
    └── .dockerignore  

---

## Services and Ports

Backend API: http://localhost:5000  
PostgreSQL: localhost:5432  
Redis: localhost:6379  

---

## Configuration

All configuration is handled using environment variables defined in docker-compose.yml.

Backend configuration:
DB_HOST=postgres  
DB_PORT=5432  
DB_NAME=appdb  
DB_USER=appuser  
DB_PASSWORD=secret  

REDIS_HOST=redis  
REDIS_PORT=6379  

PostgreSQL initialization:
POSTGRES_DB=appdb  
POSTGRES_USER=appuser  
POSTGRES_PASSWORD=secret  

Note: PostgreSQL environment variables are applied only on first initialization. If credentials change, the database volume must be recreated.

---

## Running the Application

Build and start all services:
docker compose up --build

Run in detached mode:
docker compose up -d --build

Stop containers (keep data):
docker compose down

Stop containers and remove volumes:
docker compose down -v

---

## Database Setup

Connect to PostgreSQL container:
docker exec -it postgres psql -U appuser -d appdb

Create the items table:
CREATE TABLE items (  
  id SERIAL PRIMARY KEY,  
  name TEXT NOT NULL,  
  description TEXT  
);

---

## API Endpoints

Health check:
GET /health

Response:
{ "status": "ok" }

Create item:
POST /items

Request body:
{  
  "name": "Docker",  
  "description": "Compose test"  
}

Response:
{  
  "id": 1,  
  "name": "Docker",  
  "description": "Compose test"  
}

Get item:
GET /items/{id}

First request results in a cache miss and queries PostgreSQL. Subsequent requests are served from Redis.

---

## Cache Strategy

This project uses the cache-aside pattern:

1. Backend checks Redis for cached data  
2. If cache hit → return cached value  
3. If cache miss → query PostgreSQL  
4. Store result in Redis with a TTL  
5. Return response  

Redis is treated as optional:
- If Redis is unavailable, the application still works (with reduced performance)
- If PostgreSQL is unavailable, the application fails as expected

---

## DevOps Concepts Demonstrated

- Docker build context and .dockerignore  
- Service discovery via Docker DNS  
- Container networking with user-defined bridges  
- Stateful vs stateless services  
- Persistent storage using volumes  
- Environment-based configuration  
- Real-world debugging of containerized systems  

---

## Technology Stack

Python 3.11  
Flask  
Gunicorn  
PostgreSQL 15  
Redis 7  
Docker  
Docker Compose  

---

## Notes

This project is designed for learning and demonstration purposes.  
Security hardening (secrets management, TLS, authentication) is intentionally omitted.  
The architecture can be extended with database migrations, health checks, Kubernetes deployment, and CI/CD pipelines.

---

## Summary

This project demonstrates how a real-world backend system is designed, containerized, and orchestrated using Docker Compose. It focuses on understanding system boundaries, service dependencies, configuration management, and failure scenarios rather than only application code.

