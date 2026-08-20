# Developer CLI Reference

WyFlask includes a developer CLI tool (`wyflask`) designed to automate project bootstrapping, module generation, and inspection.

---

## Global Commands

### `wyflask new <project_name>`
Scaffolds a complete production-ready WyFlask project structure.

```bash
wyflask new ecommerce_api
```

Generates:
- `app/` structure with `modules/main`, `templates/`, `static/`, and `config.py`
- `run.py` entry point with auto-registry wiring
- `.env.example`, `.gitignore`, `pyproject.toml`
- `tests/test_app.py` test suite

---

### `wyflask run`
Starts the local development server by importing `run.py` and launching the Flask application with hot-reload enabled.

```bash
wyflask run
```

---

### `wyflask routes`
Inspects the application's URL map and prints all registered endpoints, HTTP rules, and blueprint prefixes.

```bash
wyflask routes
```

Example Output:
```text
static: /static/<path:filename>
main.index: /
users.get_all: /users/
users.get_one: /users/<int:user_id>
auth.login: /auth/login
```

---

### `wyflask check`
Performs verification checks on the project configuration and health.

```bash
wyflask check
```

---

## Module Commands

### `wyflask module create <name>`
Creates a new self-contained domain module in `app/modules/<name>/`.

#### 1. Generic Module:
```bash
wyflask module create notifications
```

#### 2. REST API Module (`--api`):
Pre-configures JSON API endpoints and responses.
```bash
wyflask module create products --api
```

#### 3. HTML View Module (`--html`):
Pre-configures Jinja2 template rendering and creates `app/templates/<name>/index.html`.
```bash
wyflask module create dashboard --html
```

---

## Command Flags Cheat Sheet

| Command | Arguments | Flags | Description |
| :--- | :--- | :--- | :--- |
| `new` | `<project_name>` | — | Generate new project |
| `run` | — | — | Run local server |
| `routes` | — | — | List all registered routes |
| `check` | — | — | Run diagnostic checks |
| `module create` | `<module_name>` | `--api` | Generate REST API module |
| `module create` | `<module_name>` | `--html` | Generate HTML template module |
