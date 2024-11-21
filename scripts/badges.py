import os
import re
import subprocess
import time
import toml


# Dynamically get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the necessary files
README_FILE = os.path.join(current_dir, "../README.md")
PYPROJECT_FILE = os.path.join(current_dir, "../pyproject.toml")


def get_coverage_percentage():
    """Run pytest-cov and extract the coverage percentage from the output."""
    try:
        # Run pytest with coverage
        result = subprocess.run(
            ["pytest", "--cov=.", "--cov-report=term"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Extract coverage percentage from output using regex
        match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", result.stdout)
        if match:
            return float(match.group(1))
        else:
            print(
                "[ERROR] Could not extract coverage percentage from pytest output."
            )
            return None
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] pytest failed: {e.stderr}")
        return None


def get_version():
    """Fetch version from pyproject.toml."""
    if not os.path.exists(PYPROJECT_FILE):
        print(f"[ERROR] {PYPROJECT_FILE} not found.")
        return None
    try:
        with open(PYPROJECT_FILE) as f:
            pyproject_data = toml.load(f)
            return pyproject_data["tool"]["poetry"]["version"]
    except (KeyError, toml.TomlDecodeError) as e:
        print(f"[ERROR] Invalid format in {PYPROJECT_FILE}: {e}")
        return None


def update_badge(badge_type, new_value):
    """
    Update a badge in README.md.

    :param badge_type: Type of badge ('coverage' or 'version')
    :param new_value: Value to update the badge with
    """
    if not os.path.exists(README_FILE):
        print(f"[ERROR] {README_FILE} not found.")
        return False

    try:
        with open(README_FILE, "r") as file:
            readme_content = file.read()

        # Define badge URL
        if badge_type == "coverage":
            badge_url = f"https://img.shields.io/badge/coverage-{new_value:.2f}%25-brightgreen?cacheBust={time.time()}"
            badge_prefix = "![coverage](https://img.shields.io/badge/coverage-"
        elif badge_type == "version":
            badge_url = f"https://img.shields.io/badge/version-{new_value}-blue?cacheBust={time.time()}"
            badge_prefix = "![version](https://img.shields.io/badge/version-"
        else:
            print(f"[ERROR] Unknown badge type: {badge_type}")
            return False

        # Replace the old badge
        if badge_prefix in readme_content:
            start_index = readme_content.find(badge_prefix)
            end_index = readme_content.find(")", start_index) + 1
            full_badge = readme_content[start_index:end_index]
            updated_content = readme_content.replace(
                full_badge, f"![{badge_type}]({badge_url})"
            )
        else:
            print(
                f"[INFO] No existing {badge_type} badge found. Adding a new one."
            )
            updated_content = (
                readme_content + f"\n![{badge_type}]({badge_url})"
            )

        # Write back to README.md
        with open(README_FILE, "w") as file:
            file.write(updated_content)

        print(f"[SUCCESS] {badge_type.capitalize()} badge updated.")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to update {badge_type} badge: {e}")
        return False


if __name__ == "__main__":
    # Get coverage percentage and version
    coverage = get_coverage_percentage()
    version = get_version()

    if coverage is not None:
        update_badge("coverage", coverage)
    else:
        print("[ERROR] Coverage badge update skipped due to missing data.")

    if version is not None:
        update_badge("version", version)
    else:
        print("[ERROR] Version badge update skipped due to missing data.")
