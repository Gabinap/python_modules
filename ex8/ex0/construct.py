"""Exercise 0: Entering the Matrix - Virtual Environment Detection."""

import os
import site
import sys


def is_virtual_environment() -> bool:
    """Check if the script is running inside a virtual environment."""
    # real_prefix exists in older virtualenv-created environments
    # For venv (stdlib), base_prefix differs from prefix when active
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def display_inside_construct() -> None:
    """Display information when running inside a virtual environment."""
    # VIRTUAL_ENV is set by the activate script
    venv_path = os.environ.get("VIRTUAL_ENV")
    venv_name = os.path.basename(venv_path) if venv_path else "Unknown"
    # site-packages is where pip installs packages in this env
    site_packages = site.getsitepackages()
    packages_path = site_packages[0] if site_packages else "Unknown"

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(packages_path)


def display_outside_matrix() -> None:
    """Display information when running outside a virtual environment."""
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate  # On Unix")
    print("matrix_env\\Scripts\\activate    # On Windows")
    print()
    print("Then run this program again.")


def main() -> None:
    """Run the virtual environment detection program."""
    if is_virtual_environment():
        display_inside_construct()
    else:
        display_outside_matrix()


if __name__ == "__main__":
    main()
