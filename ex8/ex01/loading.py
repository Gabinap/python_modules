"""Exercise 01: Loading Programs - Package Management Demonstration."""

import importlib.util
import sys


# Packages required for the Matrix data analysis pipeline
REQUIRED_PACKAGES = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computing ready",
    "matplotlib": "Visualization ready",
}


def check_package(package_name: str) -> tuple[bool, str | None]:
    """Check if a package is installed and return its version."""
    # find_spec searches for a module without importing it,
    # avoiding side effects if the package is heavy or broken
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return False, None
    try:
        module = importlib.import_module(package_name)
        # Most packages expose __version__, fallback to "unknown"
        version = getattr(module, "__version__", "unknown")
        return True, version
    except ImportError:
        return False, None


def display_dependency_status() -> bool:
    """Display the status of all required dependencies."""
    print("Checking dependencies:")
    all_available = True
    for package, description in REQUIRED_PACKAGES.items():
        is_installed, version = check_package(package)
        if is_installed:
            print(f"  [OK] {package} ({version}) - {description}")
        else:
            print(f"  [MISSING] {package} - Not installed")
            all_available = False
    print()
    return all_available


def run_analysis() -> None:
    """Run a simple data analysis using the required packages."""
    import matplotlib
    import numpy as np
    import pandas as pd

    # Use non-interactive backend so plots can be saved without a display
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    print("Analyzing Matrix data...")
    np.random.seed(42)
    n_points = 1000
    print(f"Processing {n_points} data points...")

    # Simulate a noisy sine signal with 5% random anomalies
    df = pd.DataFrame(
        {
            "time": np.arange(n_points),
            "signal": np.sin(np.linspace(0, 4 * np.pi, n_points))
            + np.random.randn(n_points) * 0.3,
            "anomaly": np.random.choice([0, 1], size=n_points, p=[0.95, 0.05]),
        }
    )

    print(f"Signal mean: {df['signal'].mean():.4f}")
    print(f"Signal std: {df['signal'].std():.4f}")
    print(f"Anomalies detected: {df['anomaly'].sum()}")
    print()

    # Plot signal and highlight anomaly points in red
    print("Generating visualization...")
    _, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["time"], df["signal"], label="Signal", alpha=0.7)
    anomalies = df[df["anomaly"] == 1]
    ax.scatter(
        anomalies["time"],
        anomalies["signal"],
        color="red",
        label="Anomalies",
        zorder=5,
    )
    ax.set_xlabel("Time")
    ax.set_ylabel("Signal")
    ax.set_title("Matrix Data Analysis")
    ax.legend()
    ax.grid(True, alpha=0.3)

    output_file = "matrix_analysis.png"
    plt.savefig(output_file, dpi=100)
    plt.close()
    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    """Run the loading programs demonstration."""
    print("LOADING STATUS: Loading programs...")
    print()

    if not display_dependency_status():
        # Guide the user toward both installation methods
        print("To install with pip:")
        print("  pip install -r requirements.txt")
        print()
        print("To install with Poetry:")
        print("  poetry install")
        sys.exit(1)

    run_analysis()


if __name__ == "__main__":
    main()
