"""Extract contents from data structures."""

from pathlib import Path
import trace
from typing import Any, Dict, List, Tuple
import re
import inspect 
import importlib
import ast

from . import convert


def is_failing_test_details_empty(details: str) -> bool:
    """Determine if the string contains a newline as a hallmark of no failing tests."""
    if details == "\n":
        return True
    return False


def extract_details(details: Dict[Any, Any]) -> str:
    """Extract the details of a dictionary and return it as a string."""
    output = []
    # iterate through the dictionary and add each key-value pair
    for key, value in details.items():
        output.append(f"{value} {key}")
    if len(output) == 0:
        return ""
    return "Details: " + ", ".join(output)


def extract_test_run_details(details: Dict[Any, Any]) -> str:
    """Extract the details of a test run."""
    # Format of the data in the dictionary:
    # 'summary': Counter({'passed': 2, 'total': 2, 'collected': 2})
    summary_details = details["summary"]
    # convert the dictionary of summary to a string
    summary_details_str = extract_details(summary_details)
    return summary_details_str


def extract_test_assertion_details(test_details: Dict[Any, Any]) -> str:
    """Extract the details of a dictionary and return it as a string."""
    # create an empty list to store the output
    output = []
    # indicate that this is the first assertion
    # to be processed (it will have a "-" to start)
    first = True
    # iterate through the dictionary and add each key-value pair
    # that contains the details about the assertion
    for key, value in test_details.items():
        # this is the first assertion and thus
        # the output will start with a "-"
        if first:
            output = ["  - "]
            output.append(f"{key}: {value}\n")
            first = False
        # this is not the first assertion and thus
        # the output will start with a "  " to indent
        else:
            output.append(f"    {key}: {value}\n")
    # return each index in the output list as a string
    return "".join(output)


def extract_test_assertion_details_list(details: List[Dict[Any, Any]]) -> str:
    """Extract the details of a list of dictionaries and return it as a string."""
    output = []
    # iterate through the list of dictionaries and add each dictionary
    # to the running string that conatins test assertion details
    for current_dict in details:
        output.append(extract_test_assertion_details(current_dict))
    return "".join(output)


def extract_test_assertions_details(test_reports: List[dict[str, Any]]):
    """Extract the details of test assertions."""
    # create an empty list that will store details about
    # each test case that was execued and each of
    # the assertions that was run for that test case
    test_report_string = ""
    # iterate through the list of test reports
    # where each report is a dictionary that includes
    # the name of the test and the assertions that it ran
    for test_report in test_reports:
        # get the name of the test
        test_name = test_report["nodeid"]
        # extract only the name of the test file and the test name,
        # basically all of the content after the final slash
        display_test_name = test_name.rsplit("/", 1)[-1]
        test_report_string += f"\n{display_test_name}\n"
        # there is data about the assertions for this
        # test and thus it should be extracted and reported
        if "assertions" in test_report:
            test_report_string += extract_test_assertion_details_list(
                test_report["assertions"]
            )
    # return the string that contains all of the test assertion details
    return test_report_string


def extract_failing_test_details(
    details: dict[Any, Any],
) -> Tuple[str, List[Dict[str, Path]]]:
    """Extract the details of a failing test."""
    # extract the tests from the details
    tests = details["tests"]
    # create an empty string that starts with a newline;
    # the goal of the for loop is to incrementally build
    # of a string that contains all deteails about failing tests
    failing_details_str = "\n"
    # create an initial path for the file containing the failing test
    failing_test_paths = []
    # incrementally build up results for all of the failing tests
    for test in tests:
        if test["outcome"] == "failed":
            current_test_failing_dict = {}
            # convert the dictionary of failing details to a string
            # and add it to the failing_details_str
            failing_details = test
            # get the nodeid of the failing test
            failing_test_nodeid = failing_details["nodeid"]
            failing_details_str += f"  Name: {failing_test_nodeid}\n"
            # get the call information of the failing test
            failing_test_call = failing_details["call"]
            # get the crash information of the failing test's call
            failing_test_crash = failing_test_call["crash"]
            # extract the root of the report, which corresponds
            # to the filesystem on which the tests were run
            failing_test_path_root = details["root"]
            # extract the name of the file that contains the test
            # from the name of the individual test case itself
            failing_test_nodeid_split = failing_test_nodeid.split("::")
            # create a complete path to the file that contains the failing test file
            failing_test_path = (
                Path(failing_test_path_root) / failing_test_nodeid_split[0]
            )
            # extract the name of the function from the nodeid
            failing_test_name = failing_test_nodeid_split[-1]
            # assign the details about the failing test to the dictionary
            current_test_failing_dict["test_name"] = failing_test_name
            current_test_failing_dict["test_path"] = failing_test_path
            failing_test_paths.append(current_test_failing_dict)
            # creation additional diagnotics about the failing test
            # for further display in the console in a text-based fashion
            failing_test_path_str = convert.path_to_string(
                failing_test_path, 4
            )
            failing_test_lineno = failing_test_crash["lineno"]
            failing_test_message = failing_test_crash["message"]
            # assemble all of the failing test details into the string
            failing_details_str += f"  Path: {failing_test_path_str}\n"
            failing_details_str += f"  Line number: {failing_test_lineno}\n"
            failing_details_str += f"  Message: {failing_test_message}\n"
    # return the string that contains all of the failing test details
    return (failing_details_str, failing_test_paths)


def extract_test_output(keep_line_label: str, output: str) -> str:
    """Filter the output of the test run to keep only the lines that contain the label."""
    # create an empty string that will store the filtered output
    filtered_output = ""
    # iterate through the lines in the output
    for line in output.splitlines():
        # if the line contains the label, add it to the filtered output
        if keep_line_label in line:
            filtered_output += line + "\n"
    # return the filtered output
    return filtered_output


def extract_test_output_multiple_labels(
    keep_line_labels: List[str], output: str
) -> str:
    """Filter the output of the test run to keep only the lines that contain the label."""
    # create an empty string that will store the filtered output
    filtered_output = ""
    # iterate through the lines in the output
    for line in output.splitlines():
        # if the line contains any one of the the labels,
        # then add it to the filtered output
        if any(label in line for label in keep_line_labels):
            filtered_output += line + "\n"
    # return the filtered output
    return filtered_output

def extract_tested_functions(failing_test_code: str) -> Any:
    """Extract all functions being tested from the failing test code."""
    # Find all function calls in the code
    function_calls = re.findall(r"(\w+)\(", failing_test_code)
    # List of prefixes for functions we want to ignore
    ignore_prefixes = ["assert", "test_"]
    # Initialize a list to store valid function names
    tested_functions = set()
    # Check each function call
    for func_name in function_calls:
        # If the function name doesn't start with any ignore prefix, add it to the list
        if not any(func_name.startswith(prefix) for prefix in ignore_prefixes):
            tested_functions.add(func_name)
    # If no matching functions are found, return the full failing_test_code
    print(f'tested functions{tested_functions}')
    return tested_functions if tested_functions else failing_test_code

def get_called_functions_from_test(test_path: str) -> list[str]:
    """Get the functions called in a test from the test path."""
    # Extract the module name and function name from test_path
    module_name, func_name = test_path.split("::")
    # Import the test module
    test_module = importlib.import_module(module_name.replace("/", ".").replace(".py", ""))
    # Get the function object
    test_function = getattr(test_module, func_name)
    # Get the source code of the function
    source_code = inspect.getsource(test_function)
    # Use regex to find called functions in the source code
    called_functions = re.findall(r'\b(\w+)\s*\(', source_code)
    print(f'called functions: {called_functions}')
    return called_functions

def function_exists_in_file(file_path: str, function_name: str) -> bool:
    """Check if a function with the given name is defined in the source file."""
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
        # Parse file contents
        tree = ast.parse(file_contents)
        # Search for the function definition
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                print("Checked that function exists in file and it does!")
                return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False

def find_source_file(test_path: str, function: str) -> str:
    """ Find the source file being tested using imports"""
    test_file = test_path.split('::')[0]
    try:
        with open(test_file, 'r') as f:
            for line in f:
                if 'import' in line:
                # Extract the module being imported
                    imported = line.split('import')[-1].strip()
                    if '.' in imported:
                        imported = imported.split('.')[-1]
                    if 'from' in line:
                        imported = line.split('from')[-1].split('import')[0].strip()
                    # Skip if 'pytest' is imported
                    if imported == "pytest":
                        continue
                    # Convert module name to potential file path
                    file_path = f"{imported.replace('.', '/')}.py"
                    if file_path != "pytest.py":
                        if function_exists_in_file(file_path, function):
                            return file_path
    except Exception as e:
        print(f"Error reading file {test_file}: {e}")
    return ""

def extract_tracebacks(json_report: dict, failing_code: str) -> list:
    """Extract comprehensive test failure information from pytest JSON report including test details, assertions, variables, and complete stack traces. Handles if JSON report returns string or dictionary"""
    traceback_info_list = []
    tests = json_report.get("tests", [])
    # Go through all the tests and pull out which ones failed
    for test in tests:
        if test.get("outcome") in ("failed", "error"):
            test_path = test.get("nodeid", "")
            call = test.get("call", {})
            traceback_info = {
                "test_path": test_path,
                "source_file": "",
                "tested_function": "",
                "full_traceback": "",
                "error_type": "",
                "error_message": "",
                "stack_trace": [],
                "variables": {},
                "assertion_detail": "",
                "expected_value": None,
                "actual_value": None,
            }
            longrepr = call.get("longrepr", {})
            # Handle string longrepr
            if isinstance(longrepr, str):
                traceback_info["full_traceback"] = longrepr
                lines = longrepr.split('\n')
                # Get the name of the actual function being tested
                called_functions = get_called_functions_from_test(test_path)
                tested_funcs = extract_tested_functions(failing_code)
                print(tested_funcs)
                func = ""
                for func in tested_funcs:
                    if func in called_functions:
                        traceback_info["tested_function"] = func
                        print(f"this is the func {func}")
                        break
                # Find source file from imports
                source_file = find_source_file(test_path, func)
                if source_file:
                    traceback_info["source_file"] = source_file
                for i, line in enumerate(lines):
                    # Look for file locations in traceback
                    if "File " in line and ", line " in line:
                        loc = line.strip()
                        traceback_info["stack_trace"].append(loc)
                    # Extract error type and message
                    elif line.startswith('E   '):
                        if not traceback_info["error_message"]:
                            error_parts = line[4:].split(': ', 1)
                            if len(error_parts) > 1:
                                traceback_info["error_type"] = error_parts[0]
                                traceback_info["error_message"] = error_parts[1]
                            else:
                                traceback_info["error_message"] = error_parts[0]
                    # Look for assertion details
                    if "assert" in line:
                        traceback_info["assertion_detail"] = line.strip()
                        try:
                            if "==" in line:
                                expr = line.split("assert")[-1].strip()
                                actual, expected = expr.split("==", 1)
                                traceback_info["actual_value"] = eval(actual.strip("() "))
                                traceback_info["expected_value"] = eval(expected.strip("() "))
                        except:
                            pass
            # Handle dictionary of longrepr
            elif isinstance(longrepr, dict):
                crash = longrepr.get("reprcrash", {})
                entries = longrepr.get("reprtraceback", {}).get("reprentries", [])
                tested_funcs = extract_tested_functions(failing_code)
                called_functions = get_called_functions_from_test(test_path)
                print(tested_funcs)
                func = ""
                for func in tested_funcs:
                # Check for any mention of the function's expected behavior in the error message
                    if func in called_functions:
                        traceback_info["tested_function"] = func
                        break
                # First try to find source file from traceback entries
                source_file, = find_source_file(test_path, func)
                if source_file:
                    traceback_info["source_file"] = source_file
                # Get the error location
                line = crash.get("lineno", "")
                # Get error type and message
                message = crash.get("message", "")
                if ': ' in message:
                    error_type, error_msg = message.split(': ', 1)
                    traceback_info["error_type"] = error_type
                    traceback_info["error_message"] = error_msg
                else:
                    traceback_info["error_message"] = message
                # Build stack trace
                for entry in entries:
                    if isinstance(entry, dict):
                        loc = entry.get("reprfileloc", {})
                        if loc:
                            file_path = loc.get("path", "")
                            line_no = loc.get("lineno", "")
                            stack_entry = f"File {file_path}, line {line_no}"
                            traceback_info["stack_trace"].append(stack_entry)
            # Ensure we have a full traceback
            if not traceback_info["full_traceback"] and "log" in call:
                traceback_info["full_traceback"] = call["log"]
            # Append if there is information
            if (traceback_info["full_traceback"] or 
                traceback_info["error_message"] or 
                traceback_info["stack_trace"]):
                traceback_info_list.append(traceback_info)
    return traceback_info_list

def extract_function_code_from_traceback(traceback_info_list):
    # List to store code of each function as a list of lines
    functions = []
    for test in traceback_info_list:
        source_file = test["source_file"]
        tested_function = test["tested_function"]
        # Read the file contents
        with open(source_file, 'r') as file:
            file_contents = file.read()
        # Parse the file contents to find the function definition
        tree = ast.parse(file_contents)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == tested_function:
                # Get lines of the function's code
                function_lines = [line.strip() for line in file_contents.splitlines()[node.lineno - 1 : node.end_lineno]]
                functions.append(function_lines)
                break
    return functions

