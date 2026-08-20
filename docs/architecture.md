# Architecture & Design Patterns

WyFlask is designed around clean architecture principles, separating concerns across explicit layers while retaining the full power of Flask.

---

## High-Level Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                    Client Request                       │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              WyFlask Application Core                   │
│  - Middleware: Timing, Request-ID, Security Headers     │
│  - Error Handlers: Global exception interceptors        │
│  - Template & Static Directory Resolution               │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    Routing & Modules                    │
│  - Module (Blueprint wrapper with prefix & decorators)  │
│  - Registry (Central module store & auto-binder)        │
│  - Security: @login_required, @role_required            │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     Service Layer                       │
│  - Business logic orchestration                         │
│  - Validations, transactions, and transformations       │
│  - Base Service class                                   │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Repository Layer                      │
│  - Data access and persistence abstraction              │
│  - SQL (SQLAlchemy), NoSQL (Mongo), In-Memory           │
│  - Base Repository class                                │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Database / Storage                    │
└─────────────────────────────────────────────────────────┘
```

---

## Architectural Principles

1. **Modular Domain Design**:
   Each domain feature (e.g. `users`, `products`, `auth`) lives in its own self-contained module under `app/modules/<module_name>/`. A module encapsulates its own routes, services, repositories, schemas, and models.

2. **Decoupled Business Logic**:
   HTTP routes should only handle request parsing, calling the appropriate Service method, and formatting the response via standard helpers (`success`, `error`). Business rules never belong inside route handlers.

3. **Repository Pattern for Persistence**:
   Database interactions are encapsulated within Repositories. Swapping SQLite for PostgreSQL or MongoDB requires changing only the repository implementation, leaving services and routes untouched.

4. **Uniform API Responses**:
   All JSON API endpoints adhere to a standardized schema structure, ensuring frontend and API consumers receive predictable status codes and payloads.

5. **Centralized Error Propagation**:
   Services and repositories raise domain exceptions (`NotFoundError`, `ValidationError`, `AuthenticationError`, `AuthorizationError`). WyFlask's global error handler captures them automatically and translates them into appropriate HTTP status codes and JSON payloads.
