# API Responses & Error Handling

WyFlask standardizes JSON responses across all endpoints and provides automatic error translation for domain exceptions.

---

## Standardized JSON Response Helpers

Import helper functions from `wyflask.responses`:

```python
from wyflask.responses import success, error
```

### 1. `success()` Helper
Generates a structured 2xx JSON payload:

```python
@module.route("/products", methods=["GET"])
def get_products():
    items = [{"id": 1, "name": "Laptop", "price": 999}]
    return success(
        message="Products fetched successfully",
        data=items,
        status_code=200,
        page=1,
        total=1
    )
```

**JSON Output:**
```json
{
  "success": true,
  "message": "Products fetched successfully",
  "data": [
    {
      "id": 1,
      "name": "Laptop",
      "price": 999
    }
  ],
  "page": 1,
  "total": 1
}
```

### 2. `error()` Helper
Generates a structured error JSON payload:

```python
@module.route("/orders", methods=["POST"])
def create_order():
    # manual error response if needed
    return error(
        message="Invalid payload",
        status_code=422,
        errors={"quantity": "Must be greater than 0"}
    )
```

**JSON Output:**
```json
{
  "success": false,
  "message": "Invalid payload",
  "errors": {
    "quantity": "Must be greater than 0"
  }
}
```

---

## Framework Exceptions & Global Error Handlers

Instead of manually wrapping route handlers with `try/except` and returning error dicts, raise WyFlask domain exceptions from `wyflask.exceptions`. The framework's global error handler translates them into standard JSON error responses with appropriate HTTP status codes.

| Exception Class | Default HTTP Status | Error Code |
| :--- | :--- | :--- |
| `WyFlaskError` | 400 | `WYFLASK_ERROR` |
| `ValidationError` | 400 | `VALIDATION_ERROR` |
| `NotFoundError` | 404 | `NOT_FOUND_ERROR` |
| `AuthenticationError` | 401 | `AUTHENTICATION_ERROR` |
| `AuthorizationError` | 403 | `AUTHORIZATION_ERROR` |
| `ConfigurationError` | 400 | `CONFIGURATION_ERROR` |
| `ModuleError` | 400 | `MODULE_ERROR` |

### Example Usage:

```python
from wyflask.exceptions import NotFoundError, ValidationError

@module.route("/items/<int:item_id>")
def get_item(item_id: int):
    if item_id <= 0:
        raise ValidationError("Item ID must be a positive integer")
    
    item = find_item(item_id)
    if not item:
        raise NotFoundError(f"Item #{item_id} does not exist")
        
    return success("Item found", data=item)
```

**Response when `NotFoundError` is raised:**
- **HTTP Status**: `404 Not Found`
- **Body**:
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND_ERROR",
    "message": "Item #42 does not exist"
  }
}
```

---

## Unhandled Exceptions & Debug Mode

When an unhandled `Exception` occurs:
- In **Production** (`DEBUG = False`): Returns `500 Internal Server Error` with a safe generic message (`"An unexpected error occurred."`), preventing sensitive stack traces from leaking to clients.
- In **Development** (`DEBUG = True`): Includes `"details": str(e)` in the JSON payload to assist rapid debugging.
