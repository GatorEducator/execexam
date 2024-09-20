"""Enumerations for defining levels or options for the execexam tool."""

from enum import Enum


class AdviceMethod(str, Enum):
    """An enumeration of the ways in which advice can be sought from an LLM."""

    api_key = "apikey"
    api_server = "apiserver"


class Theme(str, Enum):
    """An enumeration of the themes for syntax highlighting in rich."""

    ansi_dark = "ansi_dark"
    ansi_light = "ansi_light"


class ReportType(str, Enum):
    """An enumeration of report types furnishing details about the exam outcomes."""

    all = "all"
    exitcode = "status"
    debug = "debug"
    finalresult = "result"
    setup = "setup"
    testcodes = "code"
    testfailures = "failure"
    testtrace = "trace"
    testadvice = "advice"
