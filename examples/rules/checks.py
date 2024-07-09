from datarules import check, Check


@check(tags=["P1", "basic"])
def check_almost_square(width, height):
    return (width - height).abs() < 5


@check(tags=["P3"])
def check_depth(depth):
    return depth < 3


# Another way to define a check
def is_even(x):
    return x % 2 == 0


# This check can be applied to multiple columns
height_is_even = Check(is_even, columns="height")
width_is_even = Check(is_even, columns="width")
depth_is_even = Check(is_even, columns="depth")
