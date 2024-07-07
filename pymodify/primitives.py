import inspect
from abc import ABCMeta

from pymodify.collector import collect_variables
from pymodify.rewriter import rewrite_expression


class Condition(metaclass=ABCMeta):
    @classmethod
    def make(cls, obj, rewrite=True):
        if isinstance(obj, cls):
            return obj
        elif callable(obj):
            return FunctionCondition(obj)
        elif isinstance(obj, str):
            return StringCondition(obj, rewrite=rewrite)
        else:
            raise TypeError


class StringCondition(Condition):
    def __init__(self, code, rewrite=True):
        if rewrite:
            code = rewrite_expression(code)
        self.code = code
        self.parameters = collect_variables(code).inputs

    def __str__(self):
        return self.code

    def __call__(self, data=None, **kwargs):
        if data is None:
            data = {}
        return eval(self.code, kwargs, data)


class FunctionCondition(Condition):
    def __init__(self, function):
        self.function = function
        self.parameters = inspect.signature(function).parameters

    def __call__(self, data=None, **kwargs):
        if data is None:
            data = kwargs
        else:
            data = {**data, **kwargs}
        data = {k: v for k, v in data.items() if k in self.parameters}
        return self.function(**data)

    def __str__(self):
        parameter_str = ", ".join(self.parameters)
        return f"{self.name}({parameter_str})"

    @property
    def name(self):
        return self.function.__name__

    @property
    def description(self):
        return inspect.getdoc(self.function)


class Action(metaclass=ABCMeta):
    @classmethod
    def make(cls, obj):
        if isinstance(obj, cls):
            return obj
        elif callable(obj):
            return FunctionAction(obj)
        elif isinstance(obj, str):
            return StringAction(obj)
        else:
            raise TypeError


class StringAction(Action):
    def __init__(self, code):
        self.code = code
        self.parameters = collect_variables(code).inputs

    def __str__(self):
        return self.code

    def __call__(self, data=None, **kwargs):
        if data is None:
            data = {}
        exec(self.code, data, kwargs)


class FunctionAction(Action):
    def __init__(self, function):
        self.function = function
        self.parameters = inspect.signature(function).parameters

    def __str__(self):
        parameter_str = ", ".join(self.parameters)
        return f"{self.name}({parameter_str})"

    def __call__(self, data=None, **kwargs):
        data = {**data, **kwargs}
        data = {k: v for k, v in data.items() if k in self.parameters}
        return self.function(**data)

    @property
    def name(self):
        return self.function.__name__

    @property
    def description(self):
        return inspect.getdoc(self.function)
