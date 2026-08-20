# Database Integration

WyFlask remains un-opinionated about the underlying persistence technology while promoting the Repository pattern. You can easily integrate **SQLAlchemy**, **SQLModel**, **Peewee**, **Tortoise**, **MongoDB (PyMongo / MongoEngine)**, or raw database drivers (like `psycopg3` or `sqlite3`).

---

## Integrating SQLAlchemy with WyFlask

### 1. Install SQLAlchemy
```bash
pip install flask-sqlalchemy
```

### 2. Configure Database in `app/config.py`
```python
import os
from wyflask.config import Config

class AppConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 3. Initialize SQLAlchemy Extension
In `app/database.py`:
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

In `run.py`:
```python
from wyflask import create_app
from wyflask.routing import registry
from app.database import db

app = create_app("app.config.AppConfig")
db.init_app(app)

with app.app_context():
    db.create_all()
```

---

## Repository Implementation with SQLAlchemy

In `app/modules/users/models.py`:
```python
from app.database import db

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
```

In `app/modules/users/repositories.py`:
```python
from wyflask.repositories import Repository
from app.database import db
from .models import UserModel
from typing import Optional

class UserRepository(Repository):
    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return UserModel.query.get(user_id)

    def get_by_username(self, username: str) -> Optional[UserModel]:
        return UserModel.query.filter_by(username=username).first()

    def create(self, username: str, email: str, password_hash: str) -> UserModel:
        user = UserModel(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
```
