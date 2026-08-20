# Quickstart Guide

Get up and running with a new WyFlask application in minutes.

---

## 1. Create a Project

Generate a structured starter project using the CLI:

```bash
wyflask new my_project
cd my_project
```

This creates the following directory structure:

```text
my_project/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── modules/
│   │   └── main/
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
│       └── index.html
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── run.py
```

---

## 2. Run the Development Server

Start the local development server:

```bash
wyflask run
```

Or execute directly with Python:

```bash
python run.py
```

Open your browser and navigate to `http://127.0.0.1:5000` to view the welcome page.

---

## 3. List Registered Routes

Inspect all active endpoints and routes in the application:

```bash
wyflask routes
```

Output:
```text
static: /static/<path:filename>
main.index: /
```

---

## 4. Scaffold a New Feature Module

Generate an API module or HTML template module:

```bash
# Generate REST API module
wyflask module create products --api

# Or generate full-stack HTML view module
wyflask module create blog --html
```

Register the new module in `run.py`:

```python
from wyflask import create_app
from wyflask.routing import registry
from app.modules.main import main_module
from app.modules.products import products_module

# Register modules
registry.register(main_module)
registry.register(products_module)

# Create Flask app
app = create_app("app.config.AppConfig")

if __name__ == "__main__":
    app.run(debug=True)
```
