import pytest
from pytest_pact.utils.pact_utils import *
from pytest_pact.utils.pytest_utils import read_marker
from pytest_pact.pact_markers import *


@pytest.hookimpl(hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    test_executor = executor(pyfuncitem)
    print('=============================')
    print(test_executor)
    test_executor.set_up()
    outcome = yield
    res = outcome.get_result()
    test_executor.tear_down()