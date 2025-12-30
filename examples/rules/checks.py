"""
There are two ways to define checks

1. Expression-checks (pass in a string or uneval.Expression)
2. Decorator checks
"""


from uneval import var
from datarules import check, Check

# Expression checks (can also be passed as str)
almost_square = Check((var.width - var.height).abs() <= 6, tags=["P1", "basic"])
not_too_deep = Check(var.depth <= 4, tags="P3")
height_is_even = Check(var.height % 2 == 0, tags="parity")


# Decorator checks
@check(tags=["P3"])
def not_too_shallow(depth):
    return depth >= 0


@check(tags=["inequality"])
def width_lt_height(width, height):
    return width < height
