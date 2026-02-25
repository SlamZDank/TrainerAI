# TrainerAI
A Django-based application for an Application backend that uses AI.

## Prerequisites

- Python 3.8+
- Podman / Docker
- PostgreSQL

## Setup

### 1. Clone the repository

### 2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  
# On Windows: .venv\Scripts\activate.ps1 like a noob 
# and a loving corporate Slopya Nutella slop
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
#### Option A: Using Podman (Recommended)
Start the PostgreSQL database:
```bash
podman-compose up -d
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

## Podman Commands

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
