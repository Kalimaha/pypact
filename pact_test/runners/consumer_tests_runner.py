import os
import imp
import inspect
from pact_test.exceptions import PactTestException


MISSING_PACT_HELPER = 'Missing "pact_helper.py" at "'
MISSING_TESTS = 'There are no consumer tests to verify.'
MISSING_SETUP = 'Missing "setup" method in "pact_helper.py".'
MISSING_TEAR_DOWN = 'Missing "tear_down" method in "pact_helper.py".'


class ConsumerTestsRunner(object):
    pact_helper = None

    def __init__(self, config):
        self.config = config

    def verify(self):
        pass

    def verify_test(self, test_class):
        test = test_class()
        test.is_valid()
        print(test.pact_uri)
        pact = self.get_pact(test.pact_uri)

    def get_pact(self, pact_uri):
        pass

    def collect_tests(self):
        root = self.config.consumer_tests_path
        files = list(filter(filter_rule, self.all_files()))
        files = list(map(lambda f: os.path.join(root, f), files))
        tests = []
        for idx, filename in enumerate(files):
            test = imp.load_source('test' + str(idx), filename)
            for name, obj in inspect.getmembers(test):
                if inspect.isclass(obj) and len(inspect.getmro(obj)) > 2:
                    test_parent = inspect.getmro(obj)[1].__name__
                    if test_parent == 'ServiceConsumerTest':
                        tests.append(obj)

        if not files:
            raise PactTestException(MISSING_TESTS)
        return tests

    def all_files(self):
        return os.listdir(self.config.consumer_tests_path)

    def load_pact_helper(self):
        self.pact_helper = imp.load_source('pact_helper', self.path_to_pact_helper())
        if hasattr(self.pact_helper, 'setup') is False:
            raise PactTestException(MISSING_SETUP)
        if hasattr(self.pact_helper, 'tear_down') is False:
            raise PactTestException(MISSING_TEAR_DOWN)

    def path_to_pact_helper(self):
        path = os.path.join(self.config.consumer_tests_path, 'pact_helper.py')
        if os.path.isfile(path) is False:
            msg = MISSING_PACT_HELPER + self.config.consumer_tests_path + '".'
            raise PactTestException(msg)
        return path


def filter_rule(filename):
    return (filename != '__init__.py' and
            filename.endswith('.py') and
            filename.endswith('pact_helper.py') is False)
