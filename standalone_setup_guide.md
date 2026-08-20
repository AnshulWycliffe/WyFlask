# Creating a Standalone App with WyFlask — Step by Step

## Step 1: Scaffold the project using the WyFlask CLI

From **any directory** (not inside the WyFlask repo), run the `wyflask new` command:

```bash
# Using the wyflask CLI from the library's venv
E:\WyFlask\venv\Scripts\wyflask.exe new taskapp
```

This creates a full project structure:

```
e:\taskapp\
├── app\
│   ├── __init__.py
│   ├── config.py
│   ├── modules\
│   │   └── main\
│   │       ├── __init__.py
│   │       └── routes.py
│   ├── templates\
│   │   └── index.html
│   └── static\
│       └── css\style.css
├── tests\
│   └── test_app.py
├── run.py
├── pyproject.toml
├── .gitignore
└── .env.example
```

---

## Step 2: Create a virtual environment for the new project

```bash
cd e:\taskapp
python -m venv venv
```

---

## Step 3: Install WyFlask as a dependency

Since `wyflask` isn't published to PyPI yet, install from local source:

```bash
.\venv\Scripts\pip.exe install e:\WyFlask
```

> [!TIP]
> Once published to PyPI, this becomes just `pip install wyflask`.

This installs `wyflask 0.1.0` plus all its dependencies (Flask, Werkzeug, etc.).

---

## Step 4: Run the app

```bash
.\venv\Scripts\wyflask.exe run
```

Output:
```
 * Serving Flask app 'wyflask.app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Open **http://127.0.0.1:5000** in your browser — you'll see the "Welcome to WyFlask" landing page.

---

## What each file does

| File | Purpose |
|---|---|
| `run.py` | Entry point — registers modules, calls `create_app()` |
| `app/config.py` | Custom config class extending `wyflask.config.Config` |
| `app/modules/main/__init__.py` | Defines `main_module = Module("main")` |
| `app/modules/main/routes.py` | Route handler: `@main_module.route("/")` |
| `app/templates/index.html` | Jinja2 template for the home page |
| `app/static/css/style.css` | Stylesheet |
| `tests/test_app.py` | Basic test using Flask test client |

---

## Key code walkthrough

### `run.py`
```python
from wyflask import create_app
from app.modules.main import main_module
from wyflask.routing import registry

registry.register(main_module)

app = create_app("app.config.AppConfig")

if __name__ == "__main__":
    app.run(debug=True)
```

### `app/modules/main/__init__.py`
```python
from wyflask.routing import Module

main_module = Module("main")

from . import routes
```

### `app/modules/main/routes.py`
```python
from flask import render_template
from . import main_module

@main_module.route("/")
def index():
    return render_template("index.html")
```

---

## Adding more modules

Use the CLI to scaffold a new module:

```bash
.\venv\Scripts\wyflask.exe module create users
```

Then register it in `run.py`:

```python
from app.modules.users import users_module
registry.register(users_module)
```
