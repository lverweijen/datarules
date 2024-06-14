from pymodify import check

h = 9


@check
def check_almost_square(width, height):
    return (width - height).abs() < 5
