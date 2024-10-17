"""Test cases for the pytest_plugin.py file."""

from typing import Any, ClassVar, Dict, List

# Global list to store test reports
reports: List[Dict[str, Any]] = []


def pytest_assertion_pass(
    item: Any, lineno: int, orig: str, expl: str
) -> None:
    """Extract and save information about a passing assertion."""
    current_test_report = next(
        (report for report in reports if report["nodeid"] == item.nodeid), None
    )
    if current_test_report is not None:
        current_assertion_dict = {"Status": "Passed"}
        if current_test_report.get("assertions") is None:
            current_test_report["assertions"] = {}
        current_test_report["assertions"][str(lineno)] = current_assertion_dict


def pytest_runtest_logreport(report):
    """Log the test report."""
    if report.when == "call":
        reports.append(
            {
                "nodeid": report.nodeid,
                "outcome": report.outcome,
                "longrepr": str(report.longrepr),
                "sections": report.sections,
            }
        )


def test_pytest_assertion_pass():
    """Test the pytest_assertion_pass function."""
    # Reset reports list
    reports.clear()

    class MockItem:
        nodeid: ClassVar[str] = "test_node"

    mock_item = MockItem()
    reports.append({"nodeid": mock_item.nodeid})

    pytest_assertion_pass(mock_item, 1, "orig", "expl")

    assert len(reports) == 1
    assert "assertions" in reports[0]
    assert "1" in reports[0]["assertions"]
    assert reports[0]["assertions"]["1"]["Status"] == "Passed"


def test_pytest_assertion_pass_no_report():
    """Test pytest_assertion_pass with no existing report."""
    # Reset reports list
    reports.clear()

    class MockItem:
        nodeid: ClassVar[str] = "test_node"

    mock_item = MockItem()

    pytest_assertion_pass(mock_item, 1, "orig", "expl")

    assert len(reports) == 0


def test_pytest_assertion_pass_no_assertions():
    """Test pytest_assertion_pass with no assertions."""
    # Reset reports list
    reports.clear()

    class MockItem:
        nodeid: ClassVar[str] = "test_node"

    mock_item = MockItem()
    reports.append({"nodeid": mock_item.nodeid})

    pytest_assertion_pass(mock_item, 1, "orig", "expl")

    assert len(reports) == 1
    assert "assertions" in reports[0]
    assert "1" in reports[0]["assertions"]
    assert reports[0]["assertions"]["1"]["Status"] == "Passed"


def test_pytest_runtest_logreport():
    """Test the pytest_runtest_logreport function."""
    # Reset reports list
    reports.clear()

    class MockReport:
        when: ClassVar[str] = "call"
        nodeid: ClassVar[str] = "test_node"
        outcome: ClassVar[str] = "passed"
        longrepr: ClassVar[str] = "long representation"
        sections: ClassVar[List[Any]] = []

    mock_report = MockReport()

    pytest_runtest_logreport(mock_report)

    assert len(reports) == 1
    assert reports[0]["nodeid"] == mock_report.nodeid
    assert reports[0]["outcome"] == mock_report.outcome
    assert reports[0]["longrepr"] == mock_report.longrepr
    assert reports[0]["sections"] == mock_report.sections


def test_pytest_runtest_logreport_not_call():
    """Test pytest_runtest_logreport with non-call event."""
    # Reset reports list
    reports.clear()

    class MockReport:
        when: ClassVar[str] = "setup"
        nodeid: ClassVar[str] = "test_node"
        outcome: ClassVar[str] = "passed"
        longrepr: ClassVar[str] = "long representation"
        sections: ClassVar[List[Any]] = []

    mock_report = MockReport()

    pytest_runtest_logreport(mock_report)

    assert len(reports) == 0
