import importlib

from . import Check, Correction
from .report import CheckReport, CorrectionReport


class Runner:
    def __init__(self):
        self.static = {}

    def import_module(self, name):
        self.static[name] = importlib.import_module(name)

    def check(self, data, checks, filter=None):
        results = self._run(data, checks, filter, Check)
        return CheckReport(results, index=getattr(data, "index", None))

    def correct(self, data, corrections, filter=None):
        results = self._run(data, corrections, filter, Correction)
        return CorrectionReport(results, index=getattr(data, "index", None))

    def _run(self, data, rules, filter, ruletype):
        for rule in rules:
            if isinstance(rule, ruletype) and (filter is None or filter(rule)):
                yield rule.run(data, **self.static)
