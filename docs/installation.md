# Installation

## Prerequisites
- **Python**: `>= 3.10`
- **Package Manager**: `pip`, `poetry`, or `uv`

---

## Installing via pip

```bash
pip install wyflask
```

For local development or editable installation from source:

```bash
git clone https://github.com/AnshulWycliffe/WyFlask.git
cd WyFlask
pip install -e .
```

---

## Verifying Installation

Verify that the CLI is installed and accessible in your shell:

```bash
wyflask --help
```

Output:
```text
usage: wyflask [-h] {new,run,shell,routes,check,module} ...

WyFlask Developer CLI

positional arguments:
  {new,run,shell,routes,check,module}
    new                 Create a new WyFlask project
    run                 Run the current application
    shell               Start an interactive shell
    routes              List registered routes
    check               Run checks on the application
    module              Module commands
```
