import inspect

from .check import Check
from .correction import Correction


def check(f=None, /, *, name=None, description=None, tags=()):
    def accept(g):
        return Check(name=name or g.__name__,
                     description=description or inspect.getdoc(g),
                     condition=g,
                     tags=tags,
                     )

    if f is None:
        return accept
    else:
        return accept(f)
    
    
def correction(f=None, /, *, condition=None, name=None, description=None, tags=()):
    def accept(g):
        return Correction(name=name or g.__name__,
                          description=description or inspect.getdoc(g),
                          condition=condition,
                          action=g,
                          tags=tags,
                          )

    if f is None:
        return accept
    else:
        return accept(f)
