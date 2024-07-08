# pymodify

## Goal and motivation

The idea of this project is to define rules to validate and correct data in pandas dataframes.
Whenever possible, it does this in a vectorized way, which makes this library really fast.


Reasons to make this:
- Implement the whole data pipeline in a single language (python).
No need to call subprocess or http to send your data to R and back.
- Directly use pandas and all other python packages you are already familiar with. No need to relearn how everything is done in R.
- Validation can be very fast if vectorized.

## Usage

This package provides two operations on data:

- checks (if data is correct). Also knows as validations.
- corrections (how to fix incorrect data)

### Checks

In checks.py
```python
from pymodify import check

@check(tags=["P1"])
def check_almost_square(width, height):
    return (width - height).abs() < 5


@check(tags=["P3", "completeness"])
def check_not_too_deep(depth):
    return depth < 3
```

In your main code:
```python
import pandas as pd
from pymodify import load_checks, Runner

df = pd.DataFrame([
    {"width": 3, "height": 7},
    {"width": 3, "height": 5, "depth": 1},
    {"width": 3, "height": 8},
    {"width": 3, "height": 3},
    {"width": 3, "height": -2, "depth": 4},
])

checks = load_checks('checks.py')
report = Runner().check(df, checks)
print(report)
```

Output:
```
                  name                           condition  items  passes  fails  NAs error  warnings
0  check_almost_square  check_almost_square(width, height)      5       3      2    0  None         0
1   check_not_too_deep           check_not_too_deep(depth)      5       1      4    0  None         0

```

### Corrections

In corrections.py
```python
from pymodify import correction
from checks import check_almost_square

@correction(condition=check_almost_square.fails)
def make_square(width, height):
    return {"height": height + (width - height) / 2}
```

In your main code:
```python
from pymodify import load_corrections

corrections = load_corrections('corrections.py')
report = Runner().correct(df, corrections)
print(report)
```

Output:
```
          name                                 condition                      action  applied error  warnings
0  make_square  check_almost_square.fails(width, height)  make_square(width, height)        2  None         0
```

## Similar work (R)

This project is inspired by https://github.com/data-cleaning/.
Similar functionality can be found in the following R packages:
 
- [dcmodify](https://github.com/data-cleaning/dcmodify)
- [validate](https://github.com/data-cleaning/validate)
- [errorlocate](https://github.com/data-cleaning/errorlocate)
- [deductive](https://github.com/data-cleaning/deductive)

Features found in one of the packages above but not implemented here, might eventually make it into this package too.

## Similar work (python)

Some offer similar functionality. However, so far none of these are vectorized on arrays.

- [Great Expectations](https://github.com/great-expectations/great_expectations) - An overengineered alternative that only does validation.
- [pyrules](https://github.com/miraculixx/pyrules) - Dead project that only does corrections.
- [pyruler](https://github.com/danteay/pyruler) - Dead project that only does validation.
- [contessa](https://github.com/kiwicom/contessa) - Does validation only. Meant to be used against databases.
- [validator](https://github.com/CSenshi/Validator) - Does validation only. Can only check variables independently.
- [python-valid8](https://github.com/smarie/python-valid8) - Does validation.
