"""
There are two ways to define checks

1. From uneval.expression.
2. Using a function
"""


from uneval import quote as q
from datarules import check, Check

# Expressions checks (can also be passed as str)
almost_square = Check((q.width - q.height).abs() <= 6, tags=["P1", "basic"])
not_too_deep = Check(q.depth <= 4, tags="P3")
height_is_even = Check(q.height % 2 == 0, tags="parity")


# Decorator checks
@check(tags=["P3"])
def not_too_shallow(depth):
    return depth >= 0


@check(tags=["inequality"])
def width_lt_height(width, height):
    return width < height
