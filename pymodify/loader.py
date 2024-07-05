from importlib.machinery import SourceFileLoader
from types import ModuleType


def load_checks(path, type="py"):
    from pymodify import Check
    if type != "py":
        raise NotImplementedError("For now only py is supported.")

    loader = SourceFileLoader("checks", path)
    module = ModuleType(loader.name)
    loader.exec_module(module)
    checklist = []
    for name, value in module.__dict__.items():
        if isinstance(value, Check):
            checklist.append(value)
    return checklist


def load_corrections(path, type="py"):
    from pymodify import Correction
    if type != "py":
        raise NotImplementedError("For now only py is supported.")

    loader = SourceFileLoader("checks", path)
    module = ModuleType(loader.name)
    loader.exec_module(module)
    correctionlist = []
    for name, value in module.__dict__.items():
        if isinstance(value, Correction):
            correctionlist.append(value)
    return correctionlist
