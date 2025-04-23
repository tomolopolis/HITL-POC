# Backend Setup Guide

This guide explains how to set up the development environment for the backend service.

## Prerequisites

- Python 3.8 or higher
- uv package manager

## Setup Instructions

1. Create a new virtual environment using uv:

```bash
uv venv
```

2. Activate the virtual environment:

```bash
# On Unix/macOS
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

3. Install dependencies using uv:

```bash
uv pip install -r pyproject.toml
```

## Running the Development Server

Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:8001
```

The API will be available at `http://localhost:8001/api/`.

## API Endpoints

- `GET /api/projects/` - List all annotation projects
- `GET /api/items/` - List annotation items (filter by project using `?project=<id>`)
- `PATCH /api/items/<id>/` - Update an annotation item's label