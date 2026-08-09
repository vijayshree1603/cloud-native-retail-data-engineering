# Cloud-Native Retail Data Engineering

A production-style retail analytics application that retains the original CSV ETL workflow and makes its loaded data available through a FastAPI service and React dashboard. It runs locally with SQLite for low-friction development and with PostgreSQL in Docker or production.

## Architecture

```mermaid
flowchart LR
  CSV["Raw retail CSV\n(local filesystem or S3-compatible storage)"] --> E[Extract]
  E --> V[Validate]
  V --> T[Transform]
  T --> P["Processed CSV"]
  T --> L[Load & verify]
  L --> DB[("PostgreSQL\nor SQLite")]
  DB --> A["FastAPI REST API"]
  A --> UI["React + Vite dashboard"]
  DB --> Q["SQL analytics"]
```

The ETL retains its extract → validate → transform → load → analytics sequence. It refuses invalid input before transformation, creates a calculated `total_amount`, writes a processed CSV, replaces and verifies the `retail_sales` table, then runs analytics. The dashboard and API read that same table.

## Quick start: complete stack with Docker

Docker Desktop is required. The Compose `etl` service waits for PostgreSQL, loads the included sample data, and exits successfully before the backend starts.

```bash
docker compose up --build
```

Open [http://localhost:8080](http://localhost:8080) for the dashboard, [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation, and [http://localhost:8000/health](http://localhost:8000/health) for health status.

Stop services with `docker compose down`. Use `docker compose down -v` only when intentionally deleting the local PostgreSQL volume.

## Local development

Requires Python 3.12+ and Node 22+.

```bash
python -m venv .venv
# PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.pipeline
uvicorn backend.app.main:app --reload
```

The default `DATABASE_URL` is a SQLite file at `data/retail_sales.db`, preserving the original one-command local ETL behavior. In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173). Copy `.env.example` to `.env` and set values for a PostgreSQL or cloud configuration; never commit `.env`.

## API

| Endpoint | Description |
|---|---|
| `GET /health` | Database-backed health check |
| `GET /api/sales?limit=25&offset=0` | Paginated sales records |
| `GET /api/analytics/total-revenue` | Total revenue |
| `GET /api/analytics/total-quantity` | Total units sold |
| `GET /api/analytics/average-order-value` | Average order value |
| `GET /api/analytics/revenue-by-category` | Revenue aggregation by category |
| `GET /api/analytics/revenue-by-region` | Revenue aggregation by region |
| `GET /api/analytics/highest-value-orders?limit=5` | Highest-value orders |

Responses are typed with Pydantic, invalid pagination is rejected by FastAPI validation, and database failures return a `503` error rather than leaking connection details.

## Database and configuration

`DATABASE_URL` accepts standard SQLAlchemy URLs. Examples:

```dotenv
# Local default (no setup required)
DATABASE_URL=sqlite:///data/retail_sales.db

# PostgreSQL / Docker
DATABASE_URL=postgresql+psycopg://retail:retail@postgres:5432/retail
```

Production credentials belong in the deployment platform’s secret store, not source control. The included Compose credentials are local-development defaults only.

## Object storage

The extraction layer uses a small `ObjectStorage` abstraction.

- `STORAGE_BACKEND=local` reads `RAW_DATA_KEY` beneath `LOCAL_STORAGE_PATH`.
- `STORAGE_BACKEND=s3` downloads `S3_PREFIX/RAW_DATA_KEY` from `S3_BUCKET` using standard boto3 credential resolution.

This supports AWS S3 and compatible providers without changing ETL code. The repository does not ship cloud credentials or claim an active cloud deployment.

## Testing and builds

```bash
# Python ETL, SQLite integration, and FastAPI tests
python -m pytest -v

# React behavior tests and production bundle
cd frontend
npm test
npm run build

# Images
docker build -f Dockerfile.backend -t retail-backend .
docker build -f Dockerfile.frontend -t retail-frontend .
```

GitHub Actions runs the Python suite, frontend test/build, and both Docker builds on pushes and pull requests to `main`; any failure fails its job.

## Deployment guidance

For AWS, run the backend and ETL job on ECS/Fargate (or Kubernetes), use RDS PostgreSQL for `DATABASE_URL`, store raw files in S3, and host the built frontend on S3 + CloudFront or a container service. Supply database URL, bucket, region/role credentials, and `CORS_ORIGINS` as environment configuration. Run the ETL as a scheduled job or an intentionally triggered task; it replaces the analytics table after validating and transforming the raw file.

The same pattern maps to Cloud Run + Cloud SQL + GCS-compatible storage, Azure Container Apps + PostgreSQL, or Kubernetes. Configure networking so only the API can reach the database and expose only the frontend/API ingress endpoints.

## Project layout

```text
backend/app/              FastAPI application and response schemas
frontend/                 Vite React dashboard and UI test
src/                      ETL, SQLAlchemy database helpers, storage abstraction
tests/                    Original ETL tests plus API integration test
data/raw/                 Versioned sample input
docker-compose.yml        PostgreSQL + ETL + API + dashboard stack
Dockerfile.backend        API/ETL image
Dockerfile.frontend       Dashboard image
```

The dashboard itself is the live visual representation of the implemented application. Add deployment-specific screenshots here after running the stack in the target environment.
