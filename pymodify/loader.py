import csv
import json
import os
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import ModuleType
from typing import Iterable, Mapping, List

from .check import Check
from .correction import Correction


def load_checks(path_or_seq: os.PathLike | Iterable[Mapping]) -> List[Check]:
    """Load checks.

    There are 2 options.
    - Load them from a python file.
    - Loaded from a list of dictionaries (useful when stored as yaml).
    """
    return _load_rules(path_or_seq, Check)


def load_corrections(path_or_seq: os.PathLike | Iterable[Mapping]) -> List[Correction]:
    """Load corrections.

    There are 2 options.
    - Load them from a python file.
    - Loaded from a list of dictionaries (useful when stored as yaml).
    """
    return _load_rules(path_or_seq, Correction)


def _load_rules(path_or_seq: os.PathLike | Iterable[Mapping], rule_type):
    if isinstance(path_or_seq, (str, os.PathLike)):
        suffix = Path(path_or_seq).suffix
        match suffix:
            case ".py":
                return _load_rules_py(path_or_seq, rule_type)
            case ".yaml":
                try:
                    import yaml
                    objects = yaml.safe_load(path_or_seq)
                except ImportError:
                    raise ImportError("Yaml not installed.")
            case ".json":
                objects = json.load(path_or_seq)
            case ".csv":
                objects = csv.DictReader(path_or_seq)
            case _:
                raise ValueError(f"Suffix {suffix} Not supported")
    else:
        objects = path_or_seq
    return _load_rules_seq(objects, rule_type)


def _load_rules_py(path, rule_type):
    loader = SourceFileLoader("rules", path)
    module = ModuleType(loader.name)
    loader.exec_module(module)
    rules = []
    for name, value in module.__dict__.items():
        if isinstance(value, rule_type):
            rules.append(value)
    return rules


def _load_rules_seq(rules, rule_type):
    if isinstance(rules, Mapping) and "rules" in rules:
        rules = rules["rules"]

    return [rule_type.from_dict(rule) for rule in rules]
