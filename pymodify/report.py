from abc import ABCMeta
from typing import Collection, TypeVar

import pandas as pd

from pymodify.check import CheckResult
from pymodify.correction import CorrectionResult
from pymodify.rule import RuleResult

TResult = TypeVar("TResult", bound=RuleResult)


class Report(Collection[TResult], metaclass=ABCMeta):
    result_cls = RuleResult

    def __init__(self, results, index=None):
        self.results = list(results)
        self.index = index

    def __contains__(self, item):
        return item in self

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def summary(self):
        return pd.DataFrame([res.summary() for res in self], columns=self.result_cls.fields)

    def print_tracebacks(self):
        for res in self:
            if res.error:
                import traceback
                traceback.print_tb(res.error.__traceback__)


class CheckReport(Report[CheckResult]):
    result_cls = CheckResult

    def dataframe(self, errors_only=True):
        df = pd.DataFrame({
            res.check.name: res.result for res in self
        }, index=self.index)

        if errors_only:
            df = df[~df.all(axis='columns')]

        return df


class CorrectionReport(Report[CorrectionResult]):
    result_cls = CorrectionResult

    def dataframe(self):
        return pd.DataFrame({
            res.correction.name: res.applied for res in self
        }, index=self.index)
