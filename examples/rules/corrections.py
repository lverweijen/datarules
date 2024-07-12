from datarules import check, correction


# This check is repeated here
@check
def almost_square(width, height):
    return (width - height).abs() < 5


@correction(trigger=almost_square.fails)
def make_square(width, height):
    """If not a square, then adjust height."""
    return {"height": height + (width - height) / 2}


@correction(trigger="depth.isna()", tags="missing")
def fill_depth(depth):
    """If depth is missing, use its mean value."""
    return {"depth": depth.mean()}
