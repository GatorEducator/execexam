import json
import toml


def get_coverage_percentage():
    with open("coverage.json") as f:
        coverage_data = json.load(f)
        total_coverage = coverage_data["totals"]["percent_covered"]
    return total_coverage


def update_coverage_badge(coverage):
    badge_url = (
        f"https://img.shields.io/badge/coverage-{coverage:.2f}%25-brightgreen"
    )
    with open("README.md", "r") as file:
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

    with open("README.md", "w") as file:
        file.write(new_readme)


def get_version():
    with open("pyproject.toml") as f:
        pyproject_data = toml.load(f)
        return pyproject_data["tool"]["poetry"]["version"]


def update_version_badge(version):
    badge_url = f"https://img.shields.io/badge/version-{version}-blue"
    with open("README.md", "r") as file:
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

    with open("README.md", "w") as file:
        file.write(new_readme)


if __name__ == "__main__":
    coverage_percentage = get_coverage_percentage()
    update_coverage_badge(coverage_percentage)

    version = get_version()
    update_version_badge(version)
