import inspect
from abc import ABCMeta, abstractmethod

from rule import Rule, make_rule, StringRule, FunctionRule

"""
@check(tags=["logical"])
def check_dimensions(width, height):
    '''Check that width is greater than height'''.
    return width > height


validator = Validator()
validator.add(check_width_gt_height)

# alternatively
validator.add("width > height",
              name="check_dimensions",
              description="Check that width is greater than height",
              tags=["logical"])
"""


class Validator:
    def __init__(self):
        self.rules = []

    def add_rule(self, *args, **kwargs):
        self.rules.append(make_validation_rule(args, **kwargs))


def check(name=None, *, description=None, tags=()):
    def accept(f):
        return make_validation_rule(f, name=name, description=description, tags=tags)

    if callable(name):
        return FunctionValidationRule(name)
    else:
        return accept


def make_validation_rule(rule, *, name=None, description=None, tags=None):
    if not isinstance(rule, ValidationRule):
        if isinstance(rule, str):
            rule = StringValidationRule(rule)
        elif callable(rule):
            rule = FunctionValidationRule(rule)
        else:
            raise TypeError(f"Unknown parameter of type {type(rule)}")

    return make_rule(rule, name=name, description=description, tags=tags)


class ValidationRule(Rule, metaclass=ABCMeta):
    def run(self, df):
        try:
            return self(df)
        except Exception as err:
            return "Error"


class FunctionValidationRule(ValidationRule, FunctionRule):
    pass
    # def __init__(self, f):
    #     super().__init__(f.__name__, description=inspect.getdoc(f))
    #     self.parameters = inspect.signature(f).parameters


class StringValidationRule(ValidationRule, StringRule):
    pass
    # def __init__(self, rule, **kwargs):
    #     self.rule = rule
    #     super().__init__(**kwargs)

    # def __call__(self, df):
    #     return df.eval(self.rule)
