# pymodify

## Goal and motivation

The idea of the project is to create similar tools as can be found on https://github.com/data-cleaning/, but to use python instead of R.

Reasons to make this:
- Implement the whole data pipeline in a single language (python).
- Directly use pandas and all other python packages you are already familiar with. No need to relearn how everything is done in R.
- No need to call subprocess or http to send your data to R and back.

## Status:

For now this package provides two operations on data:

- checks (if data is correct)
- corrections (corrections to fix data)

### Checks

In checks.py
```python
from pymodify import check

@check
def check_almost_square(width, height):
    return (width - height).abs() < 5


@check
def check_not_too_deep(depth):
    return depth < 3
```

In your main code:
```python
import pandas as pd
from pymodify import load_checks, run_checks

df = pd.DataFrame([
    {"width": 3, "height": 7},
    {"width": 3, "height": 5, "depth": 1},
    {"width": 3, "height": 8},
    {"width": 3, "height": 3},
    {"width": 3, "height": -2, "depth": 4},
])

checks = load_checks('checks.py')
report = run_checks(df, checks)
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
from pymodify import check
from checks import check_almost_square

@correction(condition=check_almost_square.fails)
def make_square(width, height):
    return {"height": height + (width - height) / 2}
```

In your main code:
```python
from pymodify import load_corrections, run_corrections

corrections = load_corrections('corrections.py')
report = run_corrections(df, checks)
print(report)
```

Output:
```
          name                                 condition                      action  applied error  warnings
0  make_square  check_almost_square.fails(width, height)  make_square(width, height)        2  None         0
```

## Similar work (R)

This package draws some inspiration from the following R packages:
 
- [dcmodify](https://github.com/data-cleaning/dcmodify)
- [validate](https://github.com/data-cleaning/validate)
- [editrules](https://github.com/data-cleaning/editrules)
- [errorlocate](https://github.com/data-cleaning/errorlocate)
- [deductive](https://github.com/data-cleaning/deductive)

Features found in one of the packages above, might eventually make it into this package too.

## Similar work (python)

- [Great Expectations](https://github.com/great-expectations/great_expectations) - An overengineered alternative that only identifies errors. It may have some good ideas, but it's not very simple to use and doesn't correct errors.
