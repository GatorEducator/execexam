import subprocess


def generate_coverage():
    # Run pytest with coverage
    command = [
        "pytest",
        "--cov=execexam",
        "--cov-report",
        "json:coverage.json",
    ]

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)

    # Check for errors
    if result.returncode != 0:
        print("Error running tests:")
        print(result.stderr)
    else:
        print("Coverage report generated: coverage.json")


if __name__ == "__main__":
    generate_coverage()
