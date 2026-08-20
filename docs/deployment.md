# Production Deployment

WyFlask creates a standard WSGI callable (`app`), making it fully compatible with all production WSGI HTTP servers, process managers, and container orchestration platforms.

---

## 1. WSGI Entry Point

Your project contains `run.py`:

```python
from wyflask import create_app
from wyflask.routing import registry
from app.modules.main import main_module
from app.modules.users import users_module

registry.register(main_module)
registry.register(users_module)

# Loads production configuration when WYFLASK_ENV=production
app = create_app("app.config.ProductionConfig")

if __name__ == "__main__":
    app.run()
```

---

## 2. Running with Gunicorn (Linux / macOS / Containers)

Install Gunicorn:
```bash
pip install gunicorn
```

Run with 4 worker processes and binding to port 8000:
```bash
export WYFLASK_ENV=production
export SECRET_KEY="your-super-secret-key-here"

gunicorn -w 4 -b 0.0.0.0:8000 'run:app'
```

---

## 3. Running with Waitress (Windows / Cross-platform)

Install Waitress:
```bash
pip install waitress
```

Run with Waitress:
```bash
waitress-serve --port=8000 run:app
```

---

## 4. Docker Deployment

Create a `Dockerfile` in the root of your project:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir gunicorn wyflask

# Copy application files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WYFLASK_ENV=production

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

Build and run:
```bash
docker build -t my-wyflask-app .
docker run -d -p 8000:8000 -e SECRET_KEY="prod-secret" my-wyflask-app
```
