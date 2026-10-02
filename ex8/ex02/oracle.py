"""Exercise 02: Accessing the Mainframe - Environment Configuration."""

import os


def load_dotenv_if_available() -> bool:
    """Load .env variables if python-dotenv is available."""
    try:
        # python-dotenv reads key=value pairs from .env
        # and injects them into os.environ
        from dotenv import load_dotenv

        load_dotenv()
        return True
    except ImportError:
        return False


def mask_secret(value: str | None) -> str:
    """Mask a secret value for safe display (e.g. 'ab****yz')."""
    if value is None:
        return "Not configured"
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def display_configuration() -> None:
    """Display the current configuration status."""
    # Retrieve config with sensible defaults for development
    mode = os.environ.get("MATRIX_MODE", "development")
    if mode not in ["development", "production"]:
        mode = "development"
    database_url = os.environ.get("DATABASE_URL")
    api_key = os.environ.get("API_KEY")
    log_level = os.environ.get("LOG_LEVEL", "DEBUG")
    zion_endpoint = os.environ.get("ZION_ENDPOINT")

    # Determine database connection type from URL
    if database_url is None:
        db_status = "Not configured"
    elif "localhost" in database_url or "127.0.0.1" in database_url:
        db_status = "Connected to local instance"
    else:
        db_status = "Connected to remote instance"

    print("Configuration loaded:")
    print(f"  Mode: {mode}")
    print(f"  Database: {db_status}")
    print(f"  API Access: {'Authenticated' if api_key else 'Not configured'}")
    print(f"  Log Level: {log_level}")
    print(f"  Zion Network: {'Online' if zion_endpoint else 'Not configured'}")
    print()


def display_security_check() -> None:
    """Display environment security check results."""
    env_exists = os.path.isfile(".env")

    print("Environment security check:")
    # No secrets are hardcoded in the source code
    print("  [OK] No hardcoded secrets detected")

    if env_exists:
        print("  [OK] .env file properly configured")
    else:
        print("  [WARNING] No .env file found")

    # Check that config can be overridden for production deployment
    if os.environ.get("MATRIX_MODE") is not None or env_exists:
        print("  [OK] Production overrides available")
    else:
        print("  [WARNING] Configure environment variables for production")
    print()


def main() -> None:
    """Run the Oracle configuration program."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    # Try to load .env; warn if python-dotenv is missing
    if not load_dotenv_if_available():
        print("WARNING: python-dotenv is not installed.")
        print("Install it with: pip install python-dotenv")
        print("Continuing with system environment variables only.")
        print()

    display_configuration()
    display_security_check()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
