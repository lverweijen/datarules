import operator

from datarules import check, Check


# First method of defining checks
@check(tags=["P1", "basic"])
def almost_square(width, height):
    return (width - height).abs() < 5


@check(tags=["P3"])
def not_too_deep(depth):
    return depth < 3


# Second method of defining checks (predicate and parameters)
def is_even(x):
    """Check if x is divisible by 2."""
    return x % 2 == 0


height_is_even = Check((is_even, "height"), tags="parity")
width_is_even = Check((is_even, "width"), tags="parity")
width_lt_height = Check((operator.lt, ["width", "height"]), tags="inequality")

# Third method of defining checks (pass code as string)
depth_is_even = Check("depth % 2 == 0", tags="parity")

# This gives an error message. However, you should still not use this on untrusted input.
# forbidden_rule = Check("open('passwords.txt').read()", tags="parity")
