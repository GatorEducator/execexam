"""Test for main module"""
import pytest
import subprocess
import sys
from pathlib import Path
from execexam.cli import cli  #

def test_run_command_with_valid_inputs(tmp_path):
    """Test the run command with valid project and test paths."""
    
    # Setup: Create temporary project and test directories
    project_dir = tmp_path / "project"
    tests_dir = tmp_path / "tests"
    project_dir.mkdir()
    tests_dir.mkdir()

    # Create dummy test files
    (project_dir / "dummy_file.py").write_text("print('This is a dummy file')")
    (tests_dir / "test_dummy.py").write_text(
        "def test_example():\n    assert True\n"
    )

    # Run the CLI command
    result = cli.invoke(cli.run, [str(project_dir), str(tests_dir)])

    # Check for successful execution
    assert result.exit_code == 0
    assert "This is the correct execexam!" in result.output

def test_run_command_with_empty_project_and_tests():
    """Test run command with empty project and tests."""
    
    # Run the CLI command with empty paths
    result = cli.invoke(cli.run, ["", ""])
    
    # Check for expected failure
    assert result.exit_code != 0
    assert "Error" in result.output  

def test_run_command_with_failing_tests(tmp_path):
    """Test run command when tests fail."""
    
    # Setup: Create temporary project and test directories
    project_dir = tmp_path / "project"
    tests_dir = tmp_path / "tests"
    project_dir.mkdir()
    tests_dir.mkdir()

    # Create a test file that will fail
    (tests_dir / "test_fail.py").write_text(
        "def test_fail():\n    assert False\n"
    )

    # Run the CLI command
    result = cli.invoke(cli.run, [str(project_dir), str(tests_dir)])

    # Check for expected failure
    assert result.exit_code != 0
    assert "Test Failure(s)" in result.output 
