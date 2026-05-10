# TrainerAI Backend

**Author:** Mohammed Amine Slama — ING A2, Groupe 4

Django REST API backend providing AI-powered fitness training services. Handles user management, workout/diet plan generation, and chat functionality.

## Features

- **User Authentication** — JWT-based authentication system
- **AI Integration** — Generates personalized workout and diet plans via AI
- **Chat API** — Real-time chat endpoint for AI assistant interactions
- **Database Management** — PostgreSQL for persistent data storage

## Tech Stack

- **Framework:** Django 5.x
- **Database:** PostgreSQL
- **Container:** Podman/Docker
- **Python:** 3.8+

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/SlamZDank/TrainerAI.git
cd TrainerAI
```

### 2. Create and activate virtual environment

```bash
source .venv/bin/activate.fish
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Update the `.env` file with your values:

```bash
DEBUG=on
SECRET_KEY=your_secret_key
URL=0.0.0.0
PORT=8080
DATABASE_URL=postgres://postgres:postgres@localhost:9500/trainer-ai
```

### 5. Start database

```bash
podman-compose up -d
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start server

```bash
python manage.py runserver
```

The backend runs on `http://127.0.0.1:8000`.

## Podman Commands

- Start database: `podman-compose up -d`
- Stop database: `podman-compose down`
- View logs: `podman-compose logs`