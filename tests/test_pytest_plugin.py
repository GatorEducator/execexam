"""Test cases for pytest_plugin.py file."""

import pytest
from typing import Any

# Global list to store test reports
reports = []

def pytest_assertion_pass(item: Any, lineno: int, orig: str, expl: str) -> None:
    """Extract and save information about a passing assertion."""
    global reports  # noqa: PLW0602
    current_test_report = {}
    for current_report in reports:
        if current_report["nodeid"] == item.nodeid:
            current_test_report = current_report
    if current_test_report != {}:
        current_assertion_dict = {}
        current_assertion_dict["Status"] = "Passed"
        if current_test_report.get("assertions") is None:
            current_test_report["assertions"] = {}
        current_test_report["assertions"][str(lineno)] = current_assertion_dict

def pytest_runtest_logreport(report):
    """Log the test report."""
    global reports  # noqa: PLW0602
    if report.when == "call":
        reports.append({
            "nodeid": report.nodeid,
            "outcome": report.outcome,
            "longrepr": str(report.longrepr),
            "sections": report.sections,
        })

# Test cases
def test_pytest_assertion_pass():
    global reports
    reports = []  # Reset reports list

    class MockItem:
        nodeid = "test_node"

    mock_item = MockItem()
    reports.append({"nodeid": mock_item.nodeid})

    pytest_assertion_pass(mock_item, 1, "orig", "expl")

    assert len(reports) == 1
    assert "assertions" in reports[0]
    assert "1" in reports[0]["assertions"]
    assert reports[0]["assertions"]["1"]["Status"] == "Passed"

def test_pytest_assertion_pass_no_report():
    global reports
    reports = []  # Reset reports list

    class MockItem:
        nodeid = "test_node"

    mock_item = MockItem()

    pytest_assertion_pass(mock_item, 1, "orig", "expl")

    assert len(reports) == 0

def test_pytest_assertion_pass_no_assertions():
    global reports
    reports = []  # Reset reports list

    class MockItem:
        nodeid = "test_node"

    mock_item = MockItem()
    reports.append({"nodeid": mock_item.nodeid})

    pytest_assertion_pass(mock_item, 1, "orig", "expl")

    assert len(reports) == 1
    assert "assertions" in reports[0]
    assert "1" in reports[0]["assertions"]
    assert reports[0]["assertions"]["1"]["Status"] == "Passed"

def test_pytest_runtest_logreport():
    global reports
    reports = []  # Reset reports list

    class MockReport:
        when = "call"
        nodeid = "test_node"
        outcome = "passed"
        longrepr = "long representation"
        sections = []

    mock_report = MockReport()

    pytest_runtest_logreport(mock_report)

    assert len(reports) == 1
    assert reports[0]["nodeid"] == mock_report.nodeid
    assert reports[0]["outcome"] == mock_report.outcome
    assert reports[0]["longrepr"] == mock_report.longrepr
    assert reports[0]["sections"] == mock_report.sections

def test_pytest_runtest_logreport_not_call():
    global reports
    reports = []  # Reset reports list

    class MockReport:
        when = "setup"
        nodeid = "test_node"
        outcome = "passed"
        longrepr = "long representation"
        sections = []

    mock_report = MockReport()

    pytest_runtest_logreport(mock_report)

    assert len(reports) == 0