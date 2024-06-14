import dataclasses
import inspect
from abc import ABCMeta
from typing import Collection


class Condition(metaclass=ABCMeta):
    @classmethod
    def make(cls, obj):
        if isinstance(obj, cls):
            return obj
        elif callable(obj):
            return FunctionCondition(obj)
        elif isinstance(obj, str):
            return StringCondition(obj)
        else:
            raise TypeError


class StringCondition(Condition):
    def __init__(self, code):
        self.code = code

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
        return self.function(**data, **kwargs)

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
        return self.function(**data, **kwargs)

    @property
    def name(self):
        return self.function.__name__

    @property
    def description(self):
        return inspect.getdoc(self.function)


@dataclasses.dataclass
class Check:
    condition: Condition
    name: str = None
    description: str = ""
    tags: Collection[str] = ()

    def __post_init__(self):
        self.condition = Condition.make(self.condition)

        if isinstance(self.condition, FunctionCondition):
            condition = self.condition
            self.name = self.name or condition.name
            self.description = self.description or condition.description

        elif self.name is None:
            self.name = f"condition_{id(self)}"

    def __call__(self, *args, **kwargs):
        return self.condition(*args, **kwargs)

    def run(self, *args, **kwargs):
        response = self(*args, **kwargs)
        return {"name": self.name,
                "condition": str(self.condition),
                "response": response}

    
@dataclasses.dataclass
class Rule:
    action: Action
    condition: Condition
    name: str = None
    description: str = ""
    tags: Collection[str] = ()

    def __post_init__(self):
        self.condition = Condition.make(self.condition)
        self.action = Action.make(self.action)

        if isinstance(self.action, FunctionAction):
            action = self.action
            self.name = self.name or action.name
            self.description = self.description or action.description
        elif self.name is None:
            self.name = f"rule_{id(self)}"

    def run(self, data):
        is_applicable = self.condition(data)
        result = self.action(data)

        for k, v in result.items():
            data.loc[is_applicable, k] = v

        return {"name": self.name,
                "condition": str(self.condition),
                "action": str(self.action),
                "applicable": is_applicable,}
