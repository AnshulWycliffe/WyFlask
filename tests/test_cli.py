import os
import shutil
import pytest
from wyflask.cli.project import create_project
from wyflask.cli.module import create_module

def test_create_project(tmp_path):
    # Change to a temp directory to avoid cluttering the real workspace
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        project_name = "test_project"
        create_project(project_name)
        assert os.path.exists(project_name)
        assert os.path.exists(os.path.join(project_name, "app", "modules", "main"))
        assert os.path.exists(os.path.join(project_name, "pyproject.toml"))
    finally:
        os.chdir(original_cwd)

def test_create_module(tmp_path):
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        os.makedirs(os.path.join("app", "modules"))
        create_module("test_mod")
        
        mod_dir = os.path.join("app", "modules", "test_mod")
        assert os.path.exists(mod_dir)
        assert os.path.exists(os.path.join(mod_dir, "__init__.py"))
        assert os.path.exists(os.path.join(mod_dir, "routes.py"))
    finally:
        os.chdir(original_cwd)
