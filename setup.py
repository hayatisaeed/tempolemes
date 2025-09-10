#!/usr/bin/env python3
import os
import subprocess
import sys
import platform
import venv
from pathlib import Path
import webbrowser


REPO_URL = "https://github.com/hayatisaeed/tempolemes.git"
PROJECT_DIR = "tempolemes"
VENV_DIR = "venv"

def run(cmd, cwd=None, shell=False):
    print(f"\n>>> Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, cwd=cwd, shell=shell)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        sys.exit(result.returncode)

def main():
    # Clone repo if not already present
    if not Path(PROJECT_DIR).exists():
        run(["git", "clone", REPO_URL])

    # Create virtualenv
    venv_path = Path(PROJECT_DIR) / VENV_DIR
    if not venv_path.exists():
        print("Creating virtual environment...")
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(venv_path)

    # Activate venv path
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        python_exe = venv_path / "bin" / "python3"
        pip_exe = venv_path / "bin" / "pip"

    # Upgrade pip & install requirements
    run([str(pip_exe), "install", "--upgrade", "pip"])
    run([str(pip_exe), "install", "-r", "requirements.txt"], cwd=PROJECT_DIR)

    # Run Django migrations
    run([str(python_exe), "manage.py", "makemigrations"], cwd=PROJECT_DIR)
    run([str(python_exe), "manage.py", "migrate"], cwd=PROJECT_DIR)

    # Create superuser (interactive)
    print("\n>>> Now creating superuser (interactive)...")
    run([str(python_exe), "manage.py", "createsuperuser"], cwd=PROJECT_DIR)

    # Run server
    print("\n>>> Starting server at http://127.0.0.1:8000/")
    run([str(python_exe), "manage.py", "runserver"], cwd=PROJECT_DIR)

    # Open browser
    webbrowser.open("http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    main()

# Example usage: python3 setup.py or python setup.py (in windows)
