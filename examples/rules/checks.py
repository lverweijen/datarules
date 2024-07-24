"""
There are a few ways to define checks

1. As an expression.
2. Using a function
3. Using a decorator
"""

import operator

from datarules import check, Check, col


# Helper for defining checks by function
def is_even(x):
    """Check if x is divisible by 2."""
    return x % 2 == 0

# 1. As an expression
almost_square = Check((col.width - col.height).abs() < 5, tags=["P1", "basic"])
not_too_deep = Check(col.depth < 3, tags="P3")

# 2. Using a function
height_is_even = Check((is_even, "height"), tags="parity")
width_is_even = Check((is_even, "width"), tags="parity")
width_lt_height = Check((operator.lt, ["width", "height"]), tags="inequality")

# 3. Using a decorator
@check(tags=["P3"])
def not_too_shallow(depth):
    return depth >= 0
