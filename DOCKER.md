# Docker Setup

## Services
- `db`: PostgreSQL 16 (`localhost:5432` inside Docker network as `db`)
- `backend`: Django + Gunicorn (`http://localhost:8000`)
- `frontend`: Vite production build served by Nginx (`http://localhost:5173`)

## Run
From the project root:

```bash
docker compose up --build
```

## Stop

```bash
docker compose down
```

To also remove database volume:

```bash
docker compose down -v
```

## Notes
- Frontend is built with `VITE_API_BASE_URL=http://localhost:8000`.
- Backend uses `DATABASE_URL=postgresql://postgres:postgres@db:5432/student_learning_hub` in Compose.
- Replace placeholder values for Google client IDs and secret key before production use.
