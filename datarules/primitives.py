import builtins
import inspect
from abc import ABCMeta
from collections.abc import Sequence

from .expression import check_expression, collect_expression, rewrite_expression


# Construct a list of safe builtins
_SAFE_BUILTINS_LIST = ['abs', 'sum', 'all', 'any', 'float', 'hex', 'int', 'bool', 'str',
                       'isinstance', 'len', 'list', 'dict', 'range', 'repr', 'reversed', 'round',
                       'set', 'slice', 'sorted', 'tuple', 'type', 'zip']
SAFE_BUILTINS = {f: getattr(builtins, f) for f in _SAFE_BUILTINS_LIST}


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
    def __init__(self, code, rewrite=True, check=True):
        if check:
            safety_analysis = check_expression(code)
            if safety_analysis.problems:
                problem_str = "\n".join(safety_analysis.problems)
                raise Exception("Code is unsafe:\n" + problem_str)
        if rewrite:
            code = rewrite_expression(code)
        self.code = code
        self.parameters = collect_expression(code).inputs

    def __str__(self):
        return self.code

    def __call__(self, data=None, **kwargs):
        if data is None:
            data = {}

        globals = {'__builtins__': SAFE_BUILTINS, **kwargs}
        return eval(self.code, globals, data)


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
    def __init__(self, code, check=True):
        if check:
            safety_analysis = check_expression(code)
            if safety_analysis.problems:
                problem_str = "\n".join(safety_analysis.problems)
                raise Exception("Code is unsafe:\n" + problem_str)
        self.code = code
        variables = collect_expression(code)
        self.parameters = variables.inputs
        self.targets = variables.outputs

    def __str__(self):
        return self.code

    def __call__(self, data=None, **kwargs):
        if data is None:
            data = {}
        else:
            data = {parameter: data[parameter] for parameter in self.parameters}

        globals = {'__builtins__': SAFE_BUILTINS, **kwargs}
        exec(self.code, globals, data)
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
