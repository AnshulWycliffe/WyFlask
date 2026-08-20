import os

def create_project(name: str):
    """Creates a new WyFlask project structure."""
    if os.path.exists(name):
        print(f"Error: Directory '{name}' already exists.")
        return

    os.makedirs(name)
    os.makedirs(os.path.join(name, "app", "modules", "main"))
    os.makedirs(os.path.join(name, "app", "templates"))
    os.makedirs(os.path.join(name, "app", "static", "css"))
    os.makedirs(os.path.join(name, "app", "static", "js"))
    os.makedirs(os.path.join(name, "app", "static", "img"))
    os.makedirs(os.path.join(name, "tests"))

    # app/__init__.py
    with open(os.path.join(name, "app", "__init__.py"), "w") as f:
        f.write("# App package")

    # app/config.py
    with open(os.path.join(name, "app", "config.py"), "w") as f:
        f.write('from wyflask.config import Config\n\nclass AppConfig(Config):\n    pass\n')

    # app/modules/main/__init__.py
    with open(os.path.join(name, "app", "modules", "main", "__init__.py"), "w") as f:
        f.write('from wyflask.routing import Module\n\nmain_module = Module("main")\n\nfrom . import routes\n')

    # app/modules/main/routes.py
    with open(os.path.join(name, "app", "modules", "main", "routes.py"), "w") as f:
        f.write('from flask import render_template\nfrom . import main_module\n\n@main_module.route("/")\ndef index():\n    return render_template("index.html")\n')

    # app/templates/index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to WyFlask</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="logo-container">
            <img class="logo" src="{{ url_for('static', filename='img/logo.png') }}" alt="WyFlask Logo" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/AnshulWycliffe/WyFlask/main/assets/logo.png';">
        </div>
        <h1>Welcome to WyFlask</h1>
        <p>Your production-grade Flask framework is ready.</p>
        <div class="links">
            <a href="https://github.com/AnshulWycliffe/WyFlask" target="_blank" rel="noopener noreferrer" class="btn primary">GitHub Repository</a>
            <a href="https://github.com/AnshulWycliffe/WyFlask#documentation" target="_blank" rel="noopener noreferrer" class="btn secondary">Documentation</a>
        </div>
        <div class="terminal">
            <div class="terminal-header">
                <span class="dot red"></span>
                <span class="dot yellow"></span>
                <span class="dot green"></span>
            </div>
            <div class="terminal-body">
                <code>wyflask module create users</code><br>
                <code>wyflask routes</code>
            </div>
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(name, "app", "templates", "index.html"), "w") as f:
        f.write(html_content)

    # app/static/css/style.css
    css_content = """
:root {
    --bg: #00273d;
    --text: #ffffff;
    --primary: #0284c7;
    --primary-hover: #0369a1;
    --secondary: #003859;
    --secondary-hover: #004d7a;
    --terminal-bg: #001e2f;
    --terminal-header: #001724;
    --border: #004166;
}

body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow: hidden;
}

.container {
    text-align: center;
    max-width: 600px;
    padding: 2rem;
}

.logo-container {
    animation: float 6s ease-in-out infinite;
    margin-bottom: 2rem;
}

.logo {
    width: 150px;
    height: auto;
    max-height: 150px;
    filter: drop-shadow(0 0 20px rgba(2, 132, 199, 0.4));
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
    100% { transform: translateY(0px); }
}

h1 {
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 1rem 0;
    color: var(--text);
    background: linear-gradient(to right, #ffffff, #7dd3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

p {
    font-size: 1.25rem;
    color: #bae6fd;
    margin-bottom: 2rem;
}

.links {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 3rem;
}

.btn {
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s;
}

.btn.primary {
    background-color: var(--primary);
    color: white;
    box-shadow: 0 4px 14px 0 rgba(2, 132, 199, 0.39);
}

.btn.primary:hover {
    background-color: var(--primary-hover);
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.23);
}

.btn.secondary {
    background-color: var(--secondary);
    color: white;
    border: 1px solid var(--border);
}

.btn.secondary:hover {
    background-color: var(--secondary-hover);
}

.terminal {
    background-color: var(--terminal-bg);
    border-radius: 0.5rem;
    overflow: hidden;
    text-align: left;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border: 1px solid var(--border);
}

.terminal-header {
    background-color: var(--terminal-header);
    padding: 0.75rem 1rem;
    display: flex;
    gap: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.dot.red { background-color: #ef4444; }
.dot.yellow { background-color: #eab308; }
.dot.green { background-color: #22c55e; }

.terminal-body {
    padding: 1.5rem;
    font-family: monospace;
    color: #f0f9ff;
    line-height: 1.5;
}

.terminal-body code::before {
    content: "$ ";
    color: #38bdf8;
}
"""
    with open(os.path.join(name, "app", "static", "css", "style.css"), "w") as f:
        f.write(css_content)


    # run.py
    with open(os.path.join(name, "run.py"), "w") as f:
        f.write('from wyflask import create_app\nfrom app.modules.main import main_module\nfrom wyflask.routing import registry\n\nregistry.register(main_module)\n\napp = create_app("app.config.AppConfig")\n\nif __name__ == "__main__":\n    app.run(debug=True)\n')

    # .env.example
    with open(os.path.join(name, ".env.example"), "w") as f:
        f.write("WYFLASK_ENV=development\nSECRET_KEY=change-this-in-production\n")

    # .gitignore
    with open(os.path.join(name, ".gitignore"), "w") as f:
        f.write("venv/\n__pycache__/\n*.pyc\n.env\n")

    # pyproject.toml
    with open(os.path.join(name, "pyproject.toml"), "w") as f:
        f.write(f'[project]\nname = "{name}"\nversion = "0.1.0"\nrequires-python = ">=3.10"\ndependencies = ["wyflask"]\n')

    # tests/test_app.py
    with open(os.path.join(name, "tests", "test_app.py"), "w") as f:
        f.write('from run import app\n\ndef test_index():\n    client = app.test_client()\n    response = client.get("/")\n    assert response.status_code == 200\n')

    print(f"Project '{name}' created successfully.")
    print(f"Run `cd {name}` and `wyflask run` to start the application.")
