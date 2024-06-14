import importlib.machinery
from types import ModuleType

from rule import Check


class Validator:
    def __init__(self):
        self.checks = []

    def add(self, *args, **kwargs):
        if args and isinstance(args[0], Check):
            check = args[0]
        else:
            check = Check(*args, **kwargs)

        self.checks.append(check)

    def update(self, checks):
        for check in checks:
            self.add(check)

    def load_py(self, path):
        loader = importlib.machinery.SourceFileLoader("checks", path)
        module = ModuleType(loader.name)
        loader.exec_module(module)
        checks = []
        for name, value in module.__dict__.items():
            if isinstance(value, Check):
                print("loading:", name)
                checks.append(value)
        self.update(checks)

    def run(self, data):
        results = []
        for check in self.checks:
            results.append(check.run(data))
        return ValidatorResult(results)


class ValidatorResult:
    def __init__(self, results):
        self._results = results

    def __iter__(self):
        return self._results

    def __str__(self):
        return str(self._results)
