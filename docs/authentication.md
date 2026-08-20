# Authentication & Security

WyFlask provides cryptographic password hashing and declarative access control decorators for authentication and role-based authorization.

---

## Password Hashing Utilities

WyFlask includes secure password hashing via `wyflask.security`:

```python
from wyflask.security import hash_password, verify_password

# 1. Hashing password on registration
raw_password = "MySecurePassword123!"
hashed = hash_password(raw_password)

# 2. Verifying password on login
is_valid = verify_password(hashed, raw_password)
# Returns True if matching, False otherwise
```

---

## Authentication Decorators

### 1. `@login_required`
Ensures that a user is authenticated before allowing access to an endpoint. It checks that `flask.g.user` is present and not `None`.

If `g.user` is missing, it raises an `AuthenticationError`, returning `401 Unauthorized`.

```python
from flask import g
from wyflask.routing import Module
from wyflask.security import login_required
from wyflask.responses import success

profile_module = Module("profile", url_prefix="/profile")

@profile_module.route("/me")
@login_required
def view_profile():
    # g.user is guaranteed to be set
    return success("Profile data", data={"user": g.user.username})
```

---

### 2. `@role_required(*roles)`
Restricts access to users who possess at least one of the specified roles. Checks `g.user.roles`.

- If `g.user` is not set: raises `AuthenticationError` (`401 Unauthorized`).
- If `g.user.roles` lacks the required roles: raises `AuthorizationError` (`403 Forbidden`).

```python
from wyflask.security import role_required
from wyflask.responses import success

admin_module = Module("admin", url_prefix="/admin")

# Single role requirement
@admin_module.route("/dashboard")
@role_required("admin")
def admin_dashboard():
    return success("Welcome to Admin Dashboard")

# Multiple acceptable roles (OR logic)
@admin_module.route("/reports")
@role_required("admin", "manager")
def view_reports():
    return success("Viewing reports")
```

---

## Authentication Middleware Example (JWT / Token / Session)

To integrate authentication with `@login_required` and `@role_required`, set `g.user` in a `before_request` hook:

```python
from flask import request, g
import jwt

class CurrentUser:
    def __init__(self, user_id: int, username: str, roles: list[str]):
        self.id = user_id
        self.username = username
        self.roles = roles

def setup_auth(app, secret_key: str):
    @app.before_request
    def load_user_from_header():
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            g.user = None
            return

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            g.user = CurrentUser(
                user_id=payload["sub"],
                username=payload["username"],
                roles=payload.get("roles", [])
            )
        except Exception:
            g.user = None
```
