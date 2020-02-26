# This file is to be executed with https://www.pyinvoke.org/
from pathlib import Path

from invoke import task

ESSENTIALS = ("git", "python3", "curl")


@task
def check_dependencies(c):
    """Check essential development dependencies are present."""
    failures = []
    for dependency in ESSENTIALS:
        try:
            c.run(f"{dependency} --version", hide=True)
        except Exception:
            failures.append(dependency)
    if failures:
        print(f"Missing essential dependencies: {failures}")


@task(check_dependencies)
def develop(c, force=False):
    """Set up a development environment."""
    if not force and (Path(c.cwd) / ".venv").is_dir():
        print(".venv directory already exists, skipping. Use --force otherwise.")
        return
    c.run("git submodule update --init --checkout --recursive")
    # Ensure poetry is installed
    try:
        c.run("poetry --version")
    except Exception:
        # Official installation method of poetry
        c.run(
            "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3"
        )
    # Use poetry to set up development environment in a local venv
    c.run("python3 -m venv .venv")
    c.run("poetry env use .venv/bin/python")
    c.run("poetry install")
    c.run("poetry run pre-commit install")


@task(develop)
def lint(c):
    """Lint & format source code."""
    c.run("poetry run pre-commit run --all-files --color=always")


@task(develop)
def test(c, verbose=False):
    """Test project."""
    flags = ["--color=yes"]
    if verbose:
        flags.append("-vv")
    flags = " ".join(flags)
    c.run(f"poetry run pytest {flags} tests")
