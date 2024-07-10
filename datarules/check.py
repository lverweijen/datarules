import dataclasses
import traceback
import warnings
from typing import Callable, Any, Optional, Sequence, Tuple

import pandas as pd

from .primitives import Condition, FunctionCondition
from .rule import Rule, RuleResult

Predicate = Callable[..., bool]


@dataclasses.dataclass(slots=True)
class Check(Rule):
    condition: Condition | str | Predicate | Tuple[Predicate, Sequence[str]]

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __post_init__(self):
        self.condition = Condition.make(self.condition)

        if isinstance(self.condition, FunctionCondition):
            condition = self.condition
            self.name = self.name or condition.name
            self.description = self.description or condition.description

        self._rule_init()

    def __call__(self, data=None, **kwargs):
        return self.condition(data, **kwargs)

    def run(self, data=None, **kwargs) -> "CheckResult":
        try:
            with warnings.catch_warnings(record=True) as wrn:
                result = self(data, **kwargs)
            error = None
        except Exception as err:
            result = None
            error = err
            traceback.print_exc()

        return CheckResult(check=self, result=result, error=error, warnings=wrn)

    @property
    def fails(self):
        return CheckFails(self)


class CheckFails(Condition):
    def __init__(self, check):
        self.check = check

    def __str__(self):
        parameter_str = ", ".join(self.parameters)
        return f"{self.check.name}.fails({parameter_str})"

    def __call__(self, data, **kwargs):
        return ~self.check(data, **kwargs)

    @property
    def name(self):
        return f"{self.check.name}.fails"

    @property
    def description(self):
        return self.check.description

    @property
    def parameters(self):
        return self.check.condition.parameters


class CheckResult(RuleResult):
    fields = ["name", "condition", "items", "passes", "fails", "NAs", "error", "warnings"]

    def __init__(self, check, result=None, error=None, warnings=()):
        self.check = check
        self.result = result
        self.error = error
        self.warnings = list(warnings)

        try:
            # Assume pd.Series
            self._value_counts = result.value_counts(dropna=False)
        except AttributeError:
            # Assume scalar
            if not error:
                self._value_counts = {result: 1}
            else:
                self._value_counts = {pd.NA: 1}

    def __repr__(self):
        output = ["<" + type(self).__name__,
                  "\n".join(f" {key}: {value}" for key, value in self.summary().items()),
                  ">"]
        return "\n".join(output)

    def summary(self):
        return {
            "name": str(self.check.name),
            "condition": str(self.check.condition),
            "items": self.items,
            "passes": self.passes,
            "fails": self.fails,
            "NAs": self.nas,
            "error": self.error,
            "warnings": len(self.warnings),
        }

    @property
    def items(self):
        try:
            return len(self.result)
        except TypeError:
            return 1

    @property
    def passes(self):
        return self._value_counts.get(True, 0)

    @property
    def fails(self):
        return self._value_counts.get(False, 0)

    @property
    def nas(self):
        return self._value_counts.get(pd.NA, 0)

    @property
    def has_error(self):
        return self.error is not None
