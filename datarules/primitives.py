import inspect
from abc import ABCMeta
from collections.abc import Sequence

from .collector import collect_variables
from .rewriter import rewrite_expression


class Condition(metaclass=ABCMeta):
    @classmethod
    def make(cls, obj):
        if isinstance(obj, cls):
            return obj
        elif callable(obj):
            return FunctionCondition(obj)
        elif isinstance(obj, str):
            return StringCondition(obj)
        elif isinstance(obj, Sequence) and callable(obj[0]):
            return FunctionCondition(*obj)
        elif isinstance(obj, Sequence) and isinstance(obj[0], str):
            return StringCondition(*obj)
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
    def __init__(self, function, parameters=None):
        self.function = function

        if parameters is None:
            parameters = inspect.signature(function).parameters
        elif isinstance(parameters, str):
            parameters = parameters.split()

        self.parameters = parameters

    def __call__(self, data=None, **kwargs):
        if data is None:
            data = kwargs
        else:
            data = {**data, **kwargs}

        args = (data[param] for param in self.parameters)
        return self.function(*args)

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
        variables = collect_variables(code)
        self.parameters = variables.inputs
        self.targets = variables.outputs

    def __str__(self):
        return self.code

    def __call__(self, data=None, **kwargs):
        if data is None:
            data = {}
        else:
            data = {parameter: data[parameter] for parameter in self.parameters}

        exec(self.code, kwargs, data)
        result = {target: data[target] for target in self.targets}
        return result


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
