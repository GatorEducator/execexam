import json
import toml
import os

# Dynamically get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the necessary files
COVERAGE_FILE = os.path.join(current_dir, "../coverage.json")
README_FILE = os.path.join(current_dir, "../README.md")
PYPROJECT_FILE = os.path.join(current_dir, "../pyproject.toml")


def get_coverage_percentage():
    if not os.path.exists(COVERAGE_FILE):
        raise FileNotFoundError(f"{COVERAGE_FILE} not found.")
    with open(COVERAGE_FILE) as f:
        coverage_data = json.load(f)
        try:
            total_coverage = coverage_data["totals"]["percent_covered"]
        except KeyError as e:
            raise KeyError(f"Expected key missing in coverage data: {e}")
    return total_coverage


def update_coverage_badge(coverage):
    badge_url = (
        f"https://img.shields.io/badge/coverage-{coverage:.2f}%25-brightgreen"
    )

    with open(README_FILE, "r") as file:
        readme_content = file.read()

    new_readme = readme_content
    old_coverage_badge = "![coverage](https://img.shields.io/badge/coverage-"
    if old_coverage_badge in readme_content:
        start_index = readme_content.find(old_coverage_badge)
        end_index = readme_content.find(")", start_index) + 1
        full_coverage_badge = readme_content[start_index:end_index]

        new_readme = readme_content.replace(
            full_coverage_badge, f"![coverage]({badge_url})"
        )

    with open(README_FILE, "w") as file:
        file.write(new_readme)


def get_version():
    if not os.path.exists(PYPROJECT_FILE):
        raise FileNotFoundError(f"{PYPROJECT_FILE} not found.")
    with open(PYPROJECT_FILE) as f:
        pyproject_data = toml.load(f)
        try:
            version = pyproject_data["tool"]["poetry"]["version"]
        except KeyError as e:
            raise KeyError(f"Expected key missing in pyproject.toml: {e}")
    return version


def update_version_badge(version):
    badge_url = f"https://img.shields.io/badge/version-{version}-blue"

    with open(README_FILE, "r") as file:
        readme_content = file.read()

    new_readme = readme_content
    old_version_badge = "![version](https://img.shields.io/badge/version-"
    if old_version_badge in readme_content:
        start_index = readme_content.find(old_version_badge)
        end_index = readme_content.find(")", start_index) + 1
        full_version_badge = readme_content[start_index:end_index]

        new_readme = readme_content.replace(
            full_version_badge, f"![version]({badge_url})"
        )

    with open(README_FILE, "w") as file:
        file.write(new_readme)


if __name__ == "__main__":
    try:
        coverage_percentage = get_coverage_percentage()
        update_coverage_badge(coverage_percentage)

        version = get_version()
        update_version_badge(version)
    except (FileNotFoundError, KeyError) as e:
        print(f"Error: {e}")
