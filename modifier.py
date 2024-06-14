import inspect
from abc import ABCMeta
from typing import Mapping

import pandas as pd

from rule import Rule, make_rule, FunctionRule, StringRule
from validator import make_validation_rule

"""
@action(tags=["logical"])
def fix_width_lt_height(width, height):
    '''Make sure that width is greater than height'''.
    return {"width": np.maximum(width, height), "height": np.minimum(width, height)}


modifier = Modifier()
modifier.add_rule(fix_width_gt_height)

# alternatively
modifier.add_rule(rule = "width += height",
                  condition="width>height",
                  name="fix_dimensions",
                  description="Check that width is greater than height",
                  tags=["logical"])
"""


class Modifier:
    def __init__(self):
        self.rules = []

    def add_rule(self, *args, **kwargs):
        self.rules.append(make_modification_rule(*args, **kwargs))

    def run(self, df, tag=None):
        rules = self.rules

        if tag:
            rules = [rule for rule in rules if tag in rule.tags]

        results = {}
        for rule in rules:
            results[rule.name] = rule.run(df)
        return ModifierResult(results)


class ModifierResult:
    def __init__(self, results):
        self.results = pd.DataFrame(results)

    def summary(self):
        summary = pd.DataFrame({k: v.value_counts() for k, v in self.results.items()})
        return summary.fillna(0).astype(int).T

    def __str__(self):
        return str(self.summary())
        # return str(self.results.value_counts())


def action(name=None, *, condition=None, description=None, tags=()):
    def accept(f):
        return make_modification_rule(f, name=name, condition=condition, description=description, tags=tags)

    if callable(name):
        return FunctionModificationRule(name)
    else:
        return accept


def make_modification_rule(rule, *, condition=None, name=None, description=None, tags=None):
    if not isinstance(rule, ModificationRule):
        if isinstance(rule, str):
            rule = StringModificationRule(rule, condition=condition)
        elif callable(rule):
            rule = FunctionModificationRule(rule)
        else:
            raise TypeError(f"Unknown parameter of type {type(rule)}")

    return make_rule(rule, name=name, description=description, tags=tags)


class ModificationRule(Rule, metaclass=ABCMeta):
    def __init__(self, *args, condition=None, **kwargs):
        if condition is not None:
            condition = make_validation_rule(condition)
        self.condition = condition
        super().__init__(*args, **kwargs)

    def run(self, df):
        if self.condition is not None:
            should_apply = self.condition(df)
        else:
            should_apply = pd.Series(True, index=df.index)

        result = self(df)
        if result is not None:
            for k, v in result.items():
                df.loc[should_apply, k] = v

        return should_apply


class FunctionModificationRule(ModificationRule, FunctionRule):
    pass
    # def act(self, df):
    #     return self.function(**df[self.parameters])


class StringModificationRule(ModificationRule, StringRule):
    pass
    # def act(self, df):
    #     df.eval(self.rule)
