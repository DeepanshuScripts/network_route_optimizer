# Network Route Optimizer API

A Django REST API for managing network nodes, edges, and shortest route optimization.

---

# Features

- Create network nodes
- Create network edges
- Find shortest route between nodes
- Store route history
- Filter route history
- Delete nodes and edges
- Standardized API responses
- RESTful architecture
- Django 5.2 LTS
- DRF-based APIs

---

# Tech Stack

| Technology | Version |
|---|---|
| Python | 3.13 |
| Django | 5.2 |
| Django REST Framework | 3.15.2 |
| SQLite/PostgreSQL | Supported |

---

# Project Structure

```text
network_route_optimizer/
│
├── config/
├── network/
│   ├── api/
│   │   └── v1/
│   │       ├── serializers.py
│   │       ├── services.py
│   │       ├── urls.py
│   │       └── views.py
│   │
│   ├── migrations/
│   ├── utils/
│   │   └── responses.py
│   │
│   ├── models.py
│   ├── urls.py
│   └── apps.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
```

---

## Create Virtual Environment

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# Run Server

```bash
python manage.py runserver
```

Server runs on:

```text
http://127.0.0.1:8000/
```

---

# API Base URL

```text
network/api/v1/
```

---

# API  Swagger Doc
http://127.0.0.1:8000/api/docs/#/

# API Redoc
http://127.0.0.1:8000/api/redoc/

---

# Architecture

The project follows layered architecture:

```text
Request
   ↓
URLs
   ↓
Views
   ↓
Serializers
   ↓
Services
   ↓
Models
   ↓
Database
```

---

# Author

Deepanshu Verma
Senior Software Developer