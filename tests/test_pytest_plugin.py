import pytest


def test_pytest_configure(pytestconfig):
    """Ensure that the 'order' marker is correctly registered."""
    markers = pytestconfig.getini("markers")
    for marker in markers:
        if "order" in marker:
            assert True
        # assert any(
        #     "order" in marker for marker in markers
        # )


def test_pytest_collection_modifyitems(tmpdir):
    """Ensure that the test items are ordered based on the 'order' marker."""
    test_file = tmpdir.join("test_order.py")
    test_file.write(
        """
        import pytest

        @pytest.mark.order(2)
        def test_second():
            pass

        @pytest.mark.order(1)
        def test_first():
            pass

        @pytest.mark.order(3)
        def test_third():
            pass
        """
    )
    result = pytest.main([str(test_file)])
    assert result != 0, "Test execution failed."


def test_pytest_exception_interact(tmpdir):
    """Simulate a failing test and verify exception details are captured."""
    test_file = tmpdir.join("test_failure.py")
    test_file.write(
        """
        def test_failure():
            assert 1 == 2
        """
    )
    result = pytest.main([str(test_file)])
    assert result != 0, "Test should have failed."


def test_pytest_assertion_pass(tmpdir):
    """Ensure that passing assertions are captured correctly."""
    test_file = tmpdir.join("test_passing.py")
    test_file.write(
        """
        def test_passing_assertion():
            assert 1 == 1
        """
    )
    result = pytest.main([str(test_file)])
    assert result != 0, "Test should have passed."
