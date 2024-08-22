# 🚀 ExecExam

ExecExam is a powerful tool that runs executable examinations in which a
student provides solutions to programming problems that are checked by Pytest
test suites. If you are a computer science or software engineering instructor
who wants to administer programming examinations

## 🌟 Main Features

- **Automated Checks**: Run a series of checks on your Python projects to
ensure they're up to standard.
- **Detailed Reports**: Get detailed reports on the results of the checks,
including which ones passed and which ones failed.
- **Advice on Failures**: If some of your code is failing the checks, ExecExam
can give you advice on what to do next.
- **Syntax Highlighting**: Enjoy syntax highlighting in the console output, with
support for both "ansi_dark" and "ansi_light" themes.
- **Verbose Mode**: Want to see more details? Just enable the verbose mode.

## 🛠️ How It Works

- **Command-line Interface**: ExecExam uses the Typer library to provide a
user-friendly command-line interface. You can specify the project directory,
test file or directory, and other options.
- **Test Collection**: ExecExam uses pytest to collect and run the tests in your
project. It supports running tests with specified marks.
- **Test Reporting**: After the tests are run, ExecExam collects detailed
information about the test runs and failures. This includes the name, path, line
number, and error message of each failing test.
- **Output Filtering**: ExecExam filters the test output to keep only the lines
that contain the label `FAILED`. This makes it easier to see which tests failed.
- **Advice on Failures**: If any tests failed, ExecExam can give you advice on
how to fix them. This feature uses a large language model to generate the
advice.
- **Exit Code**: Finally, ExecExam returns an exit code to indicate the overall
success of the examination. The exit code is `0` if all tests passed, and `1` if
any tests failed.

## ⚡️ Requirements

- Python 3.12
- Chasten leverages numerous Python packages, including notable ones such as:
    - [Rich](https://github.com/Textualize/rich): Full-featured formatting and display of text in the terminal
    - [Typer](https://github.com/tiangolo/typer): Easy-to-implement and fun-to-use command-line interfaces
- The developers of Chasten use [Poetry](https://github.com/python-poetry/poetry) for packaging and dependency management

## 🔽 Installation

Follow these steps to install the `execexam` program:

- Install Python 3.12 for your operating system
- Install [pipx](https://github.com/pypa/pipx) to support program installation in isolated environments
- Type `pipx install execexam` to install ExecExam
- Type `pipx list` and confirm that ExecExam is installed
- Type `execexam --help` to learn how to use the tool

## 🧗Improvement

- Found a bug or have a feature that the development team should implement?
[Raise an issue](https://github.com/gkapfham/execexam/issues)!
- Interesting in learning more about tool usage details? [Check the
wiki](https://github.com/gkapfham/execexam/wiki)!
- Contact [Gregory M. Kapfhammer](https://www.gregorykapfhammer.com/) with any
questions or suggestions about ExecExam!
