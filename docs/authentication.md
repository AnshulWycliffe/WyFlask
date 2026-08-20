# Authentication and Security

WyFlask provides decorators for authentication and role-based access.

```python
from wyflask.security import login_required, role_required

@login_required
def dashboard():
    pass

@role_required("admin")
def admin_panel():
    pass
```

We also provide `hash_password` and `verify_password`.
