# Quick Start Guide - Global Factor Lab

This guide will help you get Global Factor Lab up and running in under 10 minutes.

## Prerequisites Check

Before you begin, ensure you have:

- [ ] Python 3.9 or higher (`python --version`)
- [ ] Node.js 18 or higher (`node --version`)
- [ ] PostgreSQL 12 or higher (`psql --version`)
- [ ] Git (`git --version`)

## Step-by-Step Setup

### 1. Environment Setup (2 minutes)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# At minimum, update DATABASE_URL and DATA_DIR
nano .env  # or use your preferred editor
```

Example `.env`:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/global_factor_lab
DATA_DIR=/home/user/OpenPayments/data
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
NEXT_PUBLIC_API_URL=http://localhost:8000
ENVIRONMENT=development
```

### 2. Database Setup (1 minute)

```bash
# Create database
createdb global_factor_lab

# Or if using psql:
psql -U postgres -c "CREATE DATABASE global_factor_lab;"
```

### 3. Backend Setup (3 minutes)

```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Load sample data
python -m etl.load_factors --config ./etl/config/global_factor_sources.yaml

# You should see output like:
# INFO - Initialized 8 factor definitions
# INFO - Processing source: United States (US)...
# INFO - ETL pipeline completed
```

### 4. Frontend Setup (2 minutes)

```bash
# Install Node dependencies
cd ../frontend
npm install
```

### 5. Start Everything (1 minute)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Quick Test

1. Open http://localhost:3000
2. Select "United States" from dropdown
3. Click "Go"
4. You should see US factors listed
5. Click on any factor to view detailed charts

## Troubleshooting

### Database Connection Error

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Fix**: Check that PostgreSQL is running and DATABASE_URL is correct.

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Restart if needed
sudo systemctl start postgresql
```

### ETL No Files Found

```
WARNING - No files found matching pattern
```

**Fix**: Ensure sample data files exist in `data/raw/` directory.

```bash
# Check data files
ls -la data/raw/us_factors/
ls -la data/raw/sweden_factors/
ls -la data/raw/uk_factors/
```

### Port Already in Use

```
ERROR: [Errno 48] Address already in use
```

**Fix**: Kill the process using the port or change the port in `.env`.

```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or change port in .env
BACKEND_PORT=8001
```

### Node Module Errors

```
Module not found: Can't resolve '@/lib/api'
```

**Fix**: Ensure you're in the frontend directory and dependencies are installed.

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

- **Add More Data**: Follow README.md "Adding New Factor Data" section
- **Customize**: Modify factor definitions in `backend/etl/config/global_factor_sources.yaml`
- **Deploy**: See README.md "Deployment" section

## Common Commands

```bash
# Backend
cd backend
python main.py                    # Start backend
alembic upgrade head              # Run migrations
python -m etl.load_factors ...    # Load data

# Frontend
cd frontend
npm run dev                       # Development server
npm run build                     # Production build
npm start                         # Production server

# Database
createdb global_factor_lab        # Create database
dropdb global_factor_lab          # Delete database (careful!)
psql global_factor_lab            # Connect to database
```

## Getting Help

- Check the full [README.md](README.md) for detailed documentation
- Review API docs at http://localhost:8000/docs
- Open an issue on GitHub

---

Happy exploring!
