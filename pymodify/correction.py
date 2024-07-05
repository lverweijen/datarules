import dataclasses
from typing import Collection

import pandas as pd

from .primitives import Condition, FunctionAction, Action
from .check import Check


@dataclasses.dataclass(slots=True)
class Correction:
    action: Action
    condition: Condition
    name: str = None
    description: str = ""
    tags: Collection[str] = ()

    def __post_init__(self):
        if isinstance(self.condition, Check):
            raise ValueError("Check can not be used as a condition, but `check.fails` can.")

        self.condition = Condition.make(self.condition)
        self.action = Action.make(self.action)

        if isinstance(self.action, FunctionAction):
            action = self.action
            self.name = self.name or action.name
            self.description = self.description or action.description
        elif self.name is None:
            self.name = f"rule_{id(self)}"

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)

    def run(self, data):
        is_applicable = None
        error = None

        try:
            is_applicable = self.condition(data)
            result = self.action(data)
        except Exception as err:
            error = err
        else:
            for k, v in result.items():
                data.loc[is_applicable, k] = v

        return CorrectionResult(correction=self,
                                applied=is_applicable,
                                error=error,
                                warnings=())


class CorrectionResult:
    def __init__(self, correction, applied, error=None, warnings=()):
        self.correction = correction
        self.applied = applied
        self.error = error
        self.warnings = list(warnings)

    def __repr__(self):
        output = ["<" + type(self).__name__,
                  "\n".join(f" {key}: {value}" for key, value in self.summary().items()),
                  ">"]
        return "\n".join(output)

    def summary(self):
        count_applied = self.applied.astype(bool).sum()

        return {
            "name": str(self.correction.name),
            "condition": str(self.correction.condition),
            "action": str(self.correction.action),
            "applied": count_applied,
            "error": self.error,
            "warnings": len(self.warnings),
        }

    @property
    def has_error(self):
        return self.error is not None


class CorrectionReport(Collection[CorrectionResult]):
    def __init__(self, check_results, index=None):
        self.check_results = check_results
        self.index = index

    def __contains__(self, item):
        return item in self

    def __iter__(self):
        return iter(self.check_results)

    def __len__(self):
        return len(self.check_results)

    def summary(self):
        return pd.DataFrame([res.summary() for res in self])

    def dataframe(self):
        return pd.DataFrame({
            res.correction.name: res.applied for res in self
        }, index=self.index)


def run_corrections(data, correctionlist):
    results = []
    for check in correctionlist:
        results.append(check.run(data))
    return CorrectionReport(results, index=getattr(data, "index", None))
