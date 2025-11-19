# Docker Deployment Guide

This guide explains how to run Global Factor Lab using Docker and Docker Compose.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

Check your installation:
```bash
docker --version
docker-compose --version
```

## Quick Start

### 1. One-Command Startup

The easiest way to run the entire stack:

```bash
docker-compose up
```

This will:
- Start PostgreSQL database
- Build and start the FastAPI backend
- Build and start the Next.js frontend
- Run database migrations automatically
- All services will be available on localhost

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

## Docker Compose Services

### Services Included

1. **postgres** - PostgreSQL 15 database
   - Port: 5432
   - Database: global_factor_lab
   - User: postgres
   - Password: password (change in production!)

2. **backend** - FastAPI application
   - Port: 8000
   - Auto-reloads on code changes (development mode)
   - Runs migrations on startup

3. **frontend** - Next.js application
   - Port: 3000
   - Hot reload enabled

### Volumes

- `postgres_data` - Persistent PostgreSQL data
- Backend code mounted for live reload
- Frontend code mounted for live reload
- Data directory mounted at `/app/data`

## Common Commands

### Start Services

```bash
# Start in foreground (see logs)
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Start specific service
docker-compose up backend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes all data!)
docker-compose down -v
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Execute Commands in Containers

```bash
# Backend shell
docker-compose exec backend sh

# Run ETL
docker-compose exec backend python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml

# Database shell
docker-compose exec postgres psql -U postgres -d global_factor_lab

# Frontend shell
docker-compose exec frontend sh
```

## Loading Data

### Method 1: During Container Startup

The backend container automatically runs migrations. To load data:

```bash
docker-compose up -d
docker-compose exec backend python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml
```

### Method 2: Custom Data Files

Place your data files in the `data/raw/` directory on your host machine. They will be available inside the container at `/app/data/`.

```bash
# On host
cp my_factor_data.csv data/raw/my_country/

# Update config file
vim backend/etl/config/global_factor_sources.yaml

# Run ETL
docker-compose exec backend python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml
```

## Production Deployment

### 1. Update Environment Variables

Create a production `.env` file:

```env
# Database
DATABASE_URL=postgresql://postgres:STRONG_PASSWORD@postgres:5432/global_factor_lab

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
ENVIRONMENT=production

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### 2. Create Production docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: global_factor_lab
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal

  backend:
    build:
      context: ./backend
      target: production
    restart: always
    environment:
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/global_factor_lab
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    networks:
      - internal
    command: uvicorn main:app --host 0.0.0.0 --port 8000

  frontend:
    build:
      context: ./frontend
      target: runner
    restart: always
    environment:
      NEXT_PUBLIC_API_URL: ${API_URL}
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - internal

volumes:
  postgres_data:

networks:
  internal:
    driver: bridge
```

### 3. Use a Reverse Proxy

For production, use Nginx or Traefik as a reverse proxy:

```nginx
# Nginx example
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready

# View PostgreSQL logs
docker-compose logs postgres

# Restart just the database
docker-compose restart postgres
```

### Backend Won't Start

```bash
# Check backend logs
docker-compose logs backend

# Rebuild backend
docker-compose build backend
docker-compose up backend
```

### Frontend Build Errors

```bash
# Clear Next.js cache and rebuild
docker-compose exec frontend rm -rf .next
docker-compose restart frontend

# Or rebuild the image
docker-compose build --no-cache frontend
```

### Data Volume Issues

```bash
# Check volumes
docker volume ls

# Inspect volume
docker volume inspect openpayments_postgres_data

# Remove volume (WARNING: deletes all data!)
docker-compose down -v
```

## Performance Optimization

### For Production

1. **Use Production Builds**
   - Backend: Set `ENVIRONMENT=production`
   - Frontend: Build with `npm run build`

2. **Resource Limits**

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

3. **Enable Caching**
   - Use multi-stage Docker builds
   - Cache pip and npm dependencies

4. **Database Tuning**

```yaml
postgres:
  command: postgres -c shared_buffers=256MB -c max_connections=200
```

## Backup and Restore

### Backup Database

```bash
docker-compose exec postgres pg_dump -U postgres global_factor_lab > backup.sql
```

### Restore Database

```bash
cat backup.sql | docker-compose exec -T postgres psql -U postgres global_factor_lab
```

## Security Considerations

1. **Change Default Passwords**
   - Update PostgreSQL password
   - Use environment variables

2. **Network Isolation**
   - Use internal Docker networks
   - Don't expose PostgreSQL to host

3. **Regular Updates**
   ```bash
   docker-compose pull
   docker-compose up --build
   ```

4. **SSL/TLS**
   - Configure SSL for PostgreSQL
   - Use HTTPS for frontend

---

For more information, see the main [README.md](README.md).
