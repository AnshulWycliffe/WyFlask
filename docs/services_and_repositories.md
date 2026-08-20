# Services & Repositories

WyFlask provides base classes in `wyflask.services` and `wyflask.repositories` to enforce clean separation between data access and business logic.

---

## The Pattern Overview

```text
[HTTP Route]  ──►  [Service Layer]  ──►  [Repository Layer]  ──►  [Database / ORM]
(Parsing & HTTP)    (Business Rules)      (Data Queries & CRUD)    (SQL / MongoDB / Redis)
```

1. **Repository**: Only knows how to query and persist data entities.
2. **Service**: Contains business workflows, validates data invariants, calls repositories, and raises domain exceptions.
3. **Route**: Receives HTTP requests, passes arguments to services, and returns formatted responses.

---

## 1. Implementing Repositories (`wyflask.repositories.Repository`)

In `app/modules/products/repositories.py`:

```python
from wyflask.repositories import Repository
from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int

class ProductRepository(Repository):
    """Encapsulates data persistence for Products."""
    
    def __init__(self):
        # Can use SQLAlchemy db.session, Mongo client, or in-memory dict
        self._storage: dict[int, Product] = {}
        self._counter = 1

    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self._storage.get(product_id)

    def get_all(self) -> list[Product]:
        return list(self._storage.values())

    def save(self, name: str, price: float, stock: int) -> Product:
        product = Product(id=self._counter, name=name, price=price, stock=stock)
        self._storage[self._counter] = product
        self._counter += 1
        return product

    def delete(self, product_id: int) -> bool:
        return self._storage.pop(product_id, None) is not None
```

---

## 2. Implementing Services (`wyflask.services.Service`)

In `app/modules/products/services.py`:

```python
from wyflask.services import Service
from wyflask.exceptions import NotFoundError, ValidationError
from .repositories import ProductRepository, Product

class ProductService(Service):
    """Encapsulates business operations for Products."""
    
    def __init__(self, repository: ProductRepository | None = None):
        self.repo = repository or ProductRepository()

    def list_products(self) -> list[Product]:
        return self.repo.get_all()

    def get_product(self, product_id: int) -> Product:
        product = self.repo.get_by_id(product_id)
        if not product:
            raise NotFoundError(f"Product #{product_id} not found")
        return product

    def create_product(self, name: str, price: float, stock: int) -> Product:
        if not name or len(name.strip()) < 2:
            raise ValidationError("Product name must be at least 2 characters long")
        if price <= 0:
            raise ValidationError("Price must be greater than zero")
        if stock < 0:
            raise ValidationError("Stock cannot be negative")
            
        return self.repo.save(name=name.strip(), price=price, stock=stock)
```

---

## 3. Wiring into Route Handlers

In `app/modules/products/routes.py`:

```python
from flask import request
from wyflask.responses import success
from . import products_module
from .services import ProductService

service = ProductService()

@products_module.route("/", methods=["GET"])
def get_all():
    products = service.list_products()
    return success("Products fetched", data=[p.__dict__ for p in products])

@products_module.route("/<int:product_id>", methods=["GET"])
def get_one(product_id: int):
    product = service.get_product(product_id)
    return success("Product details", data=product.__dict__)

@products_module.route("/", methods=["POST"])
def create():
    data = request.get_json() or {}
    product = service.create_product(
        name=data.get("name"),
        price=float(data.get("price", 0)),
        stock=int(data.get("stock", 0))
    )
    return success("Product created", data=product.__dict__, status_code=201)
```
