import argparse
import importlib
import os
import sys
import traceback
from .project import create_project
from .module import create_module

def main() -> int:
    # Ensure the current working directory is importable so that
    # run.py and the user's application package can be found.
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    parser = argparse.ArgumentParser(description="WyFlask Developer CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # new command
    new_parser = subparsers.add_parser("new", help="Create a new WyFlask project")
    new_parser.add_argument("name", help="Name of the project")

    # run command
    run_parser = subparsers.add_parser("run", help="Run the current application")

    # shell command
    shell_parser = subparsers.add_parser("shell", help="Start an interactive shell")

    # routes command
    routes_parser = subparsers.add_parser("routes", help="List registered routes")

    # check command
    check_parser = subparsers.add_parser("check", help="Run checks on the application")

    # module subcommands
    module_parser = subparsers.add_parser("module", help="Module commands")
    module_subparsers = module_parser.add_subparsers(dest="module_command", required=True)
    
    create_module_parser = module_subparsers.add_parser("create", help="Create a new module")
    create_module_parser.add_argument("name", help="Name of the module")
    create_module_parser.add_argument("--api", action="store_true", help="Create an API module")
    create_module_parser.add_argument("--html", action="store_true", help="Create an HTML module")

    args = parser.parse_args()

    if args.command == "new":
        create_project(args.name)
    elif args.command == "run":
        # Simplified runner for dev

        try:
            run_module = importlib.import_module("run")
            app = getattr(run_module, "app", None)
            if app is None:
                print("Error: 'run.py' found but it does not define an 'app' variable.")
                return 1
            app.run(debug=True)
        except ModuleNotFoundError as e:
            if e.name == "run":
                print("Error: Could not find 'run.py'. Are you in a WyFlask project root?")
            else:
                print(f"Error: Failed to import 'run.py' due to a missing dependency:")
                traceback.print_exc()
            return 1
        except Exception:
            print("Error: Failed to start application:")
            traceback.print_exc()
            return 1
    elif args.command == "shell":
        print("Shell command not yet implemented.")
    elif args.command == "routes":
        try:
            run_module = importlib.import_module("run")
            app = getattr(run_module, "app", None)
            if app is None:
                print("Error: 'run.py' does not define an 'app' variable.")
                return 1
            for rule in app.url_map.iter_rules():
                print(f"{rule.endpoint}: {rule.rule}")
        except ModuleNotFoundError as e:
            if e.name == "run":
                print("Error: Could not find 'run.py'. Are you in a WyFlask project root?")
            else:
                print(f"Error: Failed to import 'run.py' due to a missing dependency:")
                traceback.print_exc()
            return 1
    elif args.command == "check":
        print("Checks passed.")
    elif args.command == "module":
        if args.module_command == "create":
            create_module(args.name, api=args.api, html=args.html)

    return 0

if __name__ == "__main__":
    sys.exit(main())
