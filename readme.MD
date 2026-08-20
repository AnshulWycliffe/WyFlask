# WyFlask

WyFlask is a modular, production-grade web framework built on top of Flask and Werkzeug. It provides enterprise architecture patterns, consistent API responses, built-in security, standard middleware, and a developer CLI without hiding Flask's core flexibility.

---

## Key Features

- 🏗️ **Application Factory**: Robust `create_app()` with automatic template/static path resolution.
- ⚙️ **Config Management**: Class-based and environment-driven (`WYFLASK_ENV`).
- 🧩 **Module System & Registry**: Clean abstraction over Flask Blueprints with centralized registration.
- 🛡️ **Built-in Security**: Cryptographic password hashing (`hash_password`, `verify_password`) and access decorators (`@login_required`, `@role_required`).
- 📦 **Clean Architecture**: Out-of-the-box base classes for `Service` and `Repository` patterns.
- 🎯 **Standard API Responses**: Unified `success()` and `error()` JSON payloads.
- 🚨 **Global Error Interception**: Automatic JSON formatting for domain exceptions (`NotFoundError`, `ValidationError`, `AuthenticationError`, `AuthorizationError`).
- ⏱️ **Request Lifecycle Middleware**: Automatic `X-Request-ID` tracing, `X-Process-Time` latency headers, and HTTP security headers.
- 🛠️ **Developer CLI**: Fast scaffolding with `wyflask new`, `wyflask module create`, and `wyflask routes`.

---

## Quick Installation

```bash
pip install wyflask
```

---

## Quickstart

```bash
# 1. Create a new project
wyflask new myapp
cd myapp

# 2. Run the development server
wyflask run
```

---

## Documentation

Full documentation is available in the [`docs/`](docs/index.md) folder:

- [Documentation Index](docs/index.md)
- [Installation Guide](docs/installation.md)
- [Quickstart Guide](docs/quickstart.md)
- [Architecture & Design](docs/architecture.md)
- [Configuration Management](docs/configuration.md)
- [Modules & Routing](docs/modules.md)
- [API Responses & Error Handling](docs/responses.md)
- [Middleware & Request Lifecycle](docs/middleware.md)
- [Authentication & Security](docs/authentication.md)
- [Services & Repositories](docs/services_and_repositories.md)
- [Database Integration](docs/database.md)
- [Developer CLI Reference](docs/cli.md)
- [Testing Guide](docs/testing.md)
- [Production Deployment](docs/deployment.md)
- [End-to-End Tutorial](docs/full_tutorial.md)

---

## License

MIT License. See [LICENSE](LICENSE) for details.
