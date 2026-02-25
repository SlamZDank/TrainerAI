# TrainerAI

A Django-based application for AI training and management.

## Prerequisites

- Python 3.8+
- Docker (for database)
- PostgreSQL (if not using Docker)

## Setup

### 1. Clone the repository

### 2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment configuration
Copy the environment example file:
```bash
cp .env.example .env
```

### 5. Database setup
#### Option A: Using Docker (Recommended)
Start the PostgreSQL database:
```bash
docker-compose up -d
```

#### Option B: Local PostgreSQL
Install PostgreSQL and create a database named `trainerai`.

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 8. Start the development server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Docker Commands

- Start database: `podman-compose up -d`
- Stop database: `podman-compose down`
- View logs: `podman-compose logs`

## Environment Variables

The following variables are available in `.env`:

- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `URL`: Server URL
- `PORT`: Server port
- `DATABASE_URL`: PostgreSQL connection string
