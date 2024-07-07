import importlib

from .report import CheckReport, CorrectionReport


class Runner:
    def __init__(self):
        self.static = {}

    def import_module(self, name):
        self.static[name] = importlib.import_module(name)

    def check(self, data, checks):
        results = self._run(data, checks, static=self.static)
        return CheckReport(results, index=getattr(data, "index", None))

    def correct(self, data, corrections):
        results = self._run(data, corrections, static=self.static)
        return CorrectionReport(results, index=getattr(data, "index", None))

    def _run(self, data, rules, static):
        # if static is None:
        #     static = {}

        results = []
        for rule in rules:
            print("rule = {!r}".format(rule))
            results.append(rule.run(data, **self.static))
        return results
