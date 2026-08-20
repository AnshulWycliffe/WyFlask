import os

def create_module(name: str, api: bool = False, html: bool = False):
    """Creates a new WyFlask module structure."""
    base_dir = os.path.join("app", "modules", name)
    if os.path.exists(base_dir):
        print(f"Error: Module '{name}' already exists at {base_dir}.")
        return

    os.makedirs(base_dir)

    # __init__.py
    with open(os.path.join(base_dir, "__init__.py"), "w") as f:
        url_prefix = f"/{name}"
        f.write(f'from wyflask.routing import Module\n\n{name}_module = Module("{name}", url_prefix="{url_prefix}")\n\nfrom . import routes\n')

    # routes.py
    with open(os.path.join(base_dir, "routes.py"), "w") as f:
        f.write(f'from . import {name}_module\n')
        if api:
            f.write(f'\n@{name}_module.route("/")\ndef get_{name}():\n    return {{"status": "success", "data": []}}\n')
        elif html:
            f.write(f'\nfrom flask import render_template\n\n@{name}_module.route("/")\ndef index():\n    return render_template("{name}/index.html")\n')
        else:
            f.write(f'\n@{name}_module.route("/")\ndef index():\n    return "{name.capitalize()} module"\n')

    # services.py
    with open(os.path.join(base_dir, "services.py"), "w") as f:
        f.write(f'class {name.capitalize()}Service:\n    pass\n')

    # repositories.py
    with open(os.path.join(base_dir, "repositories.py"), "w") as f:
        f.write(f'class {name.capitalize()}Repository:\n    pass\n')

    # schemas.py
    with open(os.path.join(base_dir, "schemas.py"), "w") as f:
        f.write('# Validation schemas go here\n')

    # models.py
    with open(os.path.join(base_dir, "models.py"), "w") as f:
        f.write('# Domain models go here\n')

    # templates (if html)
    if html:
        template_dir = os.path.join("app", "templates", name)
        os.makedirs(template_dir, exist_ok=True)
        with open(os.path.join(template_dir, "index.html"), "w") as f:
            f.write(f'<h1>{name.capitalize()} Module</h1>\n')

    print(f"Module '{name}' created successfully in {base_dir}.")
    print(f"Remember to register `{name}_module` in your run.py or app factory!")
