# Complete Implementation Tutorial: Building a Secure Task API

This step-by-step tutorial walks you through building a production-ready Task Management REST API using every feature of WyFlask.

---

## What We Will Build
- **Project Structure**: Clean domain modular structure.
- **Authentication**: Password hashing, JWT token verification, and `@login_required` / `@role_required` protection.
- **Task Module**: REST CRUD operations for tasks.
- **Service & Repository Layer**: Decoupled business logic and persistence.
- **Standardized Responses & Error Handling**: Domain exceptions and consistent JSON formatting.
- **Automated Tests**: Pytest test suite with client fixtures.

---

## Step 1: Scaffold the Project

Run in terminal:
```bash
wyflask new task_manager
cd task_manager
```

---

## Step 2: Create Application Modules

Generate `auth` and `tasks` modules:

```bash
wyflask module create auth --api
wyflask module create tasks --api
```

---

## Step 3: Configure Application Settings

Edit `app/config.py`:

```python
import os
from wyflask.config import Config

class AppConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-task-key")
    JWT_ALGORITHM = "HS256"

class DevelopmentConfig(AppConfig):
    DEBUG = True

class ProductionConfig(AppConfig):
    DEBUG = False
```

---

## Step 4: Implement Authentication Module

### In `app/modules/auth/repositories.py`:
```python
from wyflask.repositories import Repository
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    roles: list[str]

class UserRepository(Repository):
    def __init__(self):
        self._users: dict[str, User] = {}
        self._counter = 1

    def find_by_username(self, username: str) -> Optional[User]:
        return self._users.get(username)

    def create(self, username: str, password_hash: str, roles: list[str]) -> User:
        user = User(id=self._counter, username=username, password_hash=password_hash, roles=roles)
        self._users[username] = user
        self._counter += 1
        return user
```

### In `app/modules/auth/services.py`:
```python
import jwt
from flask import current_app
from wyflask.services import Service
from wyflask.security import hash_password, verify_password
from wyflask.exceptions import ValidationError, AuthenticationError
from .repositories import UserRepository, User

user_repo = UserRepository()

class AuthService(Service):
    def register(self, username: str, password: str, roles: list[str] | None = None) -> User:
        if not username or len(username) < 3:
            raise ValidationError("Username must be at least 3 characters")
        if not password or len(password) < 6:
            raise ValidationError("Password must be at least 6 characters")
        if user_repo.find_by_username(username):
            raise ValidationError(f"User '{username}' already exists")

        pw_hash = hash_password(password)
        return user_repo.create(username=username, password_hash=pw_hash, roles=roles or ["user"])

    def login(self, username: str, password: str) -> str:
        user = user_repo.find_by_username(username)
        if not user or not verify_password(user.password_hash, password):
            raise AuthenticationError("Invalid username or password")

        secret = current_app.config["SECRET_KEY"]
        payload = {
            "sub": user.id,
            "username": user.username,
            "roles": user.roles
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        return token
```

### In `app/modules/auth/routes.py`:
```python
from flask import request
from wyflask.responses import success
from . import auth_module
from .services import AuthService

auth_service = AuthService()

@auth_module.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    user = auth_service.register(
        username=data.get("username", ""),
        password=data.get("password", ""),
        roles=data.get("roles")
    )
    return success("User registered successfully", data={"id": user.id, "username": user.username}, status_code=201)

@auth_module.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    token = auth_service.login(
        username=data.get("username", ""),
        password=data.get("password", "")
    )
    return success("Login successful", data={"token": token})
```

---

## Step 5: Implement Task Module (With Access Control)

### In `app/modules/tasks/repositories.py`:
```python
from wyflask.repositories import Repository
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    user_id: int
    title: str
    completed: bool = False

class TaskRepository(Repository):
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._counter = 1

    def find_all_by_user(self, user_id: int) -> list[Task]:
        return [t for t in self._tasks.values() if t.user_id == user_id]

    def find_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def create(self, user_id: int, title: str) -> Task:
        task = Task(id=self._counter, user_id=user_id, title=title, completed=False)
        self._tasks[self._counter] = task
        self._counter += 1
        return task

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None
```

### In `app/modules/tasks/services.py`:
```python
from wyflask.services import Service
from wyflask.exceptions import NotFoundError, ValidationError, AuthorizationError
from .repositories import TaskRepository, Task

task_repo = TaskRepository()

class TaskService(Service):
    def get_user_tasks(self, user_id: int) -> list[Task]:
        return task_repo.find_all_by_user(user_id)

    def add_task(self, user_id: int, title: str) -> Task:
        if not title or len(title.strip()) < 1:
            raise ValidationError("Task title cannot be empty")
        return task_repo.create(user_id=user_id, title=title.strip())

    def delete_task(self, task_id: int, user_id: int, is_admin: bool = False) -> None:
        task = task_repo.find_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task #{task_id} not found")
        if task.user_id != user_id and not is_admin:
            raise AuthorizationError("You do not own this task")
        task_repo.delete(task_id)
```

### In `app/modules/tasks/routes.py`:
```python
from flask import request, g
from wyflask.responses import success
from wyflask.security import login_required
from . import tasks_module
from .services import TaskService

task_service = TaskService()

@tasks_module.route("/", methods=["GET"])
@login_required
def list_tasks():
    tasks = task_service.get_user_tasks(g.user.id)
    return success("Tasks retrieved", data=[t.__dict__ for t in tasks])

@tasks_module.route("/", methods=["POST"])
@login_required
def create_task():
    data = request.get_json() or {}
    task = task_service.add_task(user_id=g.user.id, title=data.get("title", ""))
    return success("Task created", data=task.__dict__, status_code=201)

@tasks_module.route("/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id: int):
    is_admin = "admin" in g.user.roles
    task_service.delete_task(task_id=task_id, user_id=g.user.id, is_admin=is_admin)
    return success("Task deleted successfully")
```

---

## Step 6: Auth Middleware & App Assembly

In `run.py`:

```python
import jwt
from flask import request, g
from wyflask import create_app
from wyflask.routing import registry

# Import Modules
from app.modules.main import main_module
from app.modules.auth import auth_module
from app.modules.tasks import tasks_module

# Register modules
registry.register(main_module)
registry.register(auth_module)
registry.register(tasks_module)

# Create application
app = create_app("app.config.DevelopmentConfig")

# User object helper
class AuthenticatedUser:
    def __init__(self, user_id: int, username: str, roles: list[str]):
        self.id = user_id
        self.username = username
        self.roles = roles

# JWT Authentication hook
@app.before_request
def authenticate_request():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        g.user = None
        return

    token = auth_header.split(" ")[1]
    try:
        secret = app.config["SECRET_KEY"]
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        g.user = AuthenticatedUser(
            user_id=payload["sub"],
            username=payload["username"],
            roles=payload.get("roles", [])
        )
    except Exception:
        g.user = None

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Step 7: Run & Verify with curl

1. Start server:
```bash
wyflask run
```

2. Register user:
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}'
```

3. Login & obtain token:
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}'
```

4. Create a task with JWT header:
```bash
curl -X POST http://127.0.0.1:5000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{"title": "Buy groceries"}'
```

5. Fetch tasks:
```bash
curl -X GET http://127.0.0.1:5000/tasks/ \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```
