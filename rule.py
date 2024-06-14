import inspect
from abc import ABCMeta, abstractmethod

import pandas as pd


class Rule(metaclass=ABCMeta):
    def __init__(self, name=None, description=None, tags=()):
        if name is None:
            name = "_" + hex(id(self))
        self.name = str(name).replace(" ", "_")
        self.description = str(description)
        self.tags = set(tags)

    def run(self, df):
        return self(df)

    @abstractmethod
    def __call__(self, df):
        pass


class FunctionRule(Rule, metaclass=ABCMeta):
    def __init__(self, f):
        super().__init__(f.__name__, description=inspect.getdoc(f))
        self.function = f
        self.parameters = inspect.signature(f).parameters

    def __call__(self, df=None, /, **kwargs):
        if df is not None:
            return self.function(**df, **kwargs)
        else:
            return self.function(**kwargs)


class StringRule(Rule, metaclass=ABCMeta):
    def __init__(self, rule, **kwargs):
        self.rule = rule
        super().__init__(**kwargs)

    def __call__(self, df=None, /, **kwargs):
        if df is not None:
            return df.eval(self.rule)
        else:
            return pd.eval(self.rule, resolvers=[kwargs])


def make_rule(rule, *, name=None, description=None, tags=None):
    if not isinstance(rule, Rule):
        print("rule = {!r}".format(rule))
        raise TypeError("This is not a rule")

    if name:
        rule.name = name
    if description:
        rule.description = description
    if tags:
        rule.tags.update(tags)

    return rule
