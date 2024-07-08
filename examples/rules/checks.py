from pymodify import check


@check(tags=["P1", "basic"])
def check_almost_square(width, height):
    return (width - height).abs() < 5


@check(tags=["P3"])
def check_depth(depth):
    return depth < 3
