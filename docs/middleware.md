# Middleware & Request Lifecycle

WyFlask provides automatic request instrumentation, unique trace tracking, execution latency measurement, and security headers out of the box.

---

## Default Middleware Stack

When `create_app()` initializes your application, it registers standard request hooks:

```python
from wyflask.middleware import register_middleware
```

### 1. Request ID Tracking (`X-Request-ID`)
- Intercepts incoming `X-Request-ID` headers from reverse proxies (e.g. Nginx, Cloudflare, AWS ALB).
- If no header is supplied, generates a unique UUIDv4 string.
- Attaches the ID to `flask.g.request_id`.
- Injects the `X-Request-ID` into every HTTP response header for distributed tracing and log correlation.

### 2. Request Timing (`X-Process-Time`)
- Records timestamp at the beginning of each request (`g.start_time`).
- Computes total elapsed execution time upon completion.
- Injects the elapsed time in seconds into the `X-Process-Time` response header.

### 3. Essential Security Headers
Sets industry-standard HTTP security headers on all outgoing responses:
- `X-Content-Type-Options: nosniff` (prevents MIME-type sniffing)
- `X-Frame-Options: SAMEORIGIN` (mitigates clickjacking attacks)
- `X-XSS-Protection: 1; mode=block` (enables cross-site scripting filter)

---

## Accessing Request ID in Handlers and Services

You can access the current request's unique identifier via Flask's global context object `g`:

```python
from flask import g
from wyflask.utils import get_logger

logger = get_logger("orders")

@orders_module.route("/checkout", methods=["POST"])
def checkout():
    req_id = getattr(g, "request_id", "N/A")
    logger.info(f"Processing checkout for request [{req_id}]")
    return success("Order placed successfully")
```

---

## Adding Custom Middleware

You can attach custom hooks using standard Flask decorators or by registering a custom middleware function:

```python
from flask import request, g

def register_custom_middleware(app):
    @app.before_request
    def inspect_api_version():
        g.api_version = request.headers.get("X-API-Version", "v1")
```
