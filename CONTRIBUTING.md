# For Contributors

## Welcome

Welcome to the `Contributors Guide` for Execexam!

## Getting Started

To contribute to Execexam, you must have [Python 3.11 or later](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/) installed.

To set up a development environment for `execexam`, first clone the Execexam repository.

`git clone git@github.com:GatorEducator/execexam.git`

Then, in your copy of `execexam`, run poetry install. This will install all of Execexam's runtime and development dependencies. Now, you can begin to contribute to the GatorGrade project following the guidelines below.

## Links to Resources

## Contributing Changes

### GitHub Flow

Execexam is maintained using the [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow) workflow. This means that before making any changes to your copy of Execexam, you should [create a new branch](https://docs.github.com/en/get-started/quickstart/github-flow#create-a-branch) off of the main branch. The name of the branch should be a short, descriptive name that describes the changes you plan on making in the branch. For example, if you are planning to update the README.md, you might name your branch update-readme. Notice that the branch name should be all lowercase and have words separated by hyphens.

### Testing Changes

Running Execexam Locally
As you make changes, you will want to see how they affect the output of Execexam. To do this, in the branch that contains your changes, run:

`poetry build`
This will build an archive (i.e. a release artifact) of Execexam that contains your changes. To use this archive, you can install it with pipx:

`pipx install dist/execexam-<archive-version>.whl`
Then, you can run the `execexam` commands in any assignment repository to view the output of Execexam with your changes.

If you have already done this, have made additional changes, and would like to try out your most recent changes, we recommend that you first uninstall Execexam with pipx:

`pipx uninstall execexam`
Then, you can proceed with building and installing a new Execexam archive.

### Running the Test Suite

You should also test that your changes have not caused any regressions in the Execexam system. You can do this by running:

`poetry run task test`
This will run the test task defined in the pyproject.toml, which will execute all of the tests. You can be confident that your changes have not caused any regressions if all tests pass.

Additionally, you should lint your changes to make sure they follow the stylistic rules of the Execexam project. You can do this by running:

`poetry run task lint`
This will run the lint task, which executes various linters such as pylint, that ensure that the style of your changes matches the rest of GatorGrade. Any linting errors that appear should be addressed.

### Committing Changes

As you make and test changes, you should be making small, focused, and targeted commits. Additionally, commit messages should follow these guidelines:

Should be 50 characters or less (soft limit - exceptions include co-author or function names for example)
Should be in the imperative mood
Should be void of all grammatical and spelling mistakes

### Pull Requests

Once you have finished making and committing your changes to your branch, you should [create a pull request](https://docs.github.com/en/get-started/quickstart/github-flow#create-a-pull-request) so that others can review your changes. Before creating a pull request, make sure that the last commit in your branch produced a passing build in GitHub Actions. When you create a pull request, please make sure to fill out all portions of the template.

### Bug Reports

Please submit your bug reports using the [GitHub Issue Tracker](https://github.com/GatorEducator/execexam/issues). Use the bug template for submission guidelines.

### Feature Suggestions

Please submit your feature suggestions using the [GitHub Issue Tracker](https://github.com/GatorEducator/execexam/issues). Use the feature request template for submission guidelines.

## Code of Conduct

Please refer to our `CODE_OF_CONDUCT.md` for our guidelines on conduct.

## Thank You

Big thank you to everyone who has contributed to this project thus far!

## Owner Information

If you would like to contact the owner of this project please message `@gkapfham` for more information.
