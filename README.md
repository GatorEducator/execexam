# 🚀 ExecExam

<img src="https://i.ibb.co/vzjX7p2/exe.png" alt="logo" height="500">

[![coverage](https://img.shields.io/badge/coverage-20.86%25-brightgreen)](https://github.com/GatorEducator/execexam/actions)
[![Static Badge](https://img.shields.io/badge/Maintained%3F-yes-orange)](https://github.com/GatorEducator/execexam/commits/main/)
![version](https://img.shields.io/badge/version-0.3.0-blue)


ExecExam is a powerful tool that runs executable examinations in which a
student provides solutions to programming problems that are checked by Pytest
test suites. If you are a computer science or software engineering instructor
who wants to administer programming examinations

## 🌟 Main Features

- **Automated Checks**: Run a series of checks on your Python projects to ensure
they're up to standard.
- **Detailed Reports**: See the results of the checks, including which ones
passed and which ones failed.
- **Advice on Failures**: When code fails a check, receive advice on what to do next.
- **Syntax Highlighting**: Enjoy syntax highlighting in the console output.
- **Verbose Mode**: Want to see more details? Just enable the verbose mode!

## 🤝 LLM-Based Advice

ExecExam uses the LLM-based advice system to provide students with feedback
when one of their answers fails a check. You can either specify the complete
URL of a LiteLLM API proxy or set an API key for a cloud-based LLM provider.
Here are examples of some of the LLM models that are supported through the use
of [LiteLLM](https://docs.litellm.ai/docs/providers):

- `anthropic/claude-3-haiku-20240307`
- `anthropic/claude-3-opus-20240229`
- `groq/llama3-8b-8192`
- `openrouter/meta-llama/llama-3.1-8b-instruct:free`
- `openrouter/google/gemma-2-9b-it:free`

## 🔧 Requirements

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

## Contributing to Execexam

If you would like to contribute to Execexam, please refer to the [Execexam Wiki](https://github.com/GatorEducator/gatorgrade/wiki/Contributing-Guidelines) for contributing guidelines.
