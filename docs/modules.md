# Modules

WyFlask Modules are abstractions over Flask Blueprints.

```python
from wyflask.routing import Module

my_module = Module("my_module", url_prefix="/my_module")

@my_module.route("/")
def index():
    return "Hello"
```
