"""Testing for enumeration file"""
import pytest
from enum import Enum

from execexam.enumerations import (
    AdviceMethod,
    Theme,
    ReportType
)


def test_advice_method_enum_values():
    """Confirm that AdviceMethod enum has the correct values."""
    assert AdviceMethod.api_key.value == "apikey"
    assert AdviceMethod.api_server.value == "apiserver"


def test_advice_method_enum_access_by_name():
    """Confirm that AdviceMethod enum members are accessible by name."""
    assert AdviceMethod["api_key"] == AdviceMethod.api_key
    assert AdviceMethod["api_server"] == AdviceMethod.api_server


def test_advice_method_enum_invalid_name():
    """Confirm that accessing an invalid name in AdviceMethod raises KeyError."""
    with pytest.raises(KeyError):
        _ = AdviceMethod["invalid"]


def test_theme_enum_values():
    """Confirm that Theme enum has the correct values."""
    assert Theme.ansi_dark.value == "ansi_dark"
    assert Theme.ansi_light.value == "ansi_light"


def test_theme_enum_access_by_name():
    """Confirm that Theme enum members are accessible by name."""
    assert Theme["ansi_dark"] == Theme.ansi_dark
    assert Theme["ansi_light"] == Theme.ansi_light


def test_theme_enum_invalid_name():
    """Confirm that accessing an invalid name in Theme raises KeyError."""
    with pytest.raises(KeyError):
        _ = Theme["invalid"]


def test_report_type_enum_values():
    """Confirm that ReportType enum has the correct values."""
    assert ReportType.all.value == "all"
    assert ReportType.exitcode.value == "status"
    assert ReportType.finalresult.value == "result"
    assert ReportType.testcodes.value == "code"
    assert ReportType.testfailures.value == "failure"
    assert ReportType.testtrace.value == "trace"
    assert ReportType.testadvice.value == "advice"
    assert ReportType.setup.value == "setup"


def test_report_type_enum_access_by_name():
    """Confirm that ReportType enum members are accessible by name."""
    assert ReportType["all"] == ReportType.all
    assert ReportType["exitcode"] == ReportType.exitcode
    assert ReportType["finalresult"] == ReportType.finalresult
    assert ReportType["testcodes"] == ReportType.testcodes
    assert ReportType["testfailures"] == ReportType.testfailures
    assert ReportType["testtrace"] == ReportType.testtrace
    assert ReportType["testadvice"] == ReportType.testadvice
    assert ReportType["setup"] == ReportType.setup


def test_report_type_enum_invalid_name():
    """Confirm that accessing an invalid name in ReportType raises KeyError."""
    with pytest.raises(KeyError):
        _ = ReportType["invalid"]