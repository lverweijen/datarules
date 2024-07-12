# DataRules

## Goal and motivation

The idea of this project is to define rules to validate and correct datasets.
Whenever possible, it does this in a vectorized way, which makes this library fast.


Reasons to make this:
- Implement an alternative to https://github.com/data-cleaning/ based on python and pandas.
- Implement both validation and correction. Most existing packages provide validation only.
- Support a rule based way of data processing. The rules can be maintained in a separate file (python or yaml) if required.
- Apply vectorization to make processing fast.

## Usage

This package provides two operations on data:

- checks (if data is correct). Also knows as validations.
- corrections (how to fix incorrect data)

### Checks

In checks.py

```python
from datarules import check


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
from datarules import CheckList

df = pd.DataFrame([
    {"width": 3, "height": 7},
    {"width": 3, "height": 5, "depth": 1},
    {"width": 3, "height": 8},
    {"width": 3, "height": 3},
    {"width": 3, "height": -2, "depth": 4},
])

checks = CheckList.from_file('checks.py')
report = checks.run(df)
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
from datarules import correction
from checks import check_almost_square


@correction(condition=check_almost_square.fails)
def make_square(width, height):
    return {"height": height + (width - height) / 2}
```

In your main code:

```python
from datarules import CorrectionList

corrections = CorrectionList.from_file('corrections.py')
report = corrections.run(df)
print(report)
```

Output:
```
          name                                 condition                      action  applied error  warnings
0  make_square  check_almost_square.fails(width, height)  make_square(width, height)        2  None         0
```

## Similar work (python)

These work on pandas, but only do validation:

- [Pandera](https://pandera.readthedocs.io/en/stable/index.html) - Like us, their checks are also vectorized.
- [Pandantic](https://github.com/wesselhuising/pandantic) - Combination of validation and parsing based on [pydantic](https://docs.pydantic.dev/latest/).

The following offer validation only, but none of them seem to be vectorized or support pandas directly.

- [Great Expectations](https://github.com/great-expectations/great_expectations) - An overengineered library for validation that has confusing documentation.
- [contessa](https://github.com/kiwicom/contessa) - Meant to be used against databases.
- [validator](https://github.com/CSenshi/Validator)
- [python-valid8](https://github.com/smarie/python-valid8)
- [pyruler](https://github.com/danteay/pyruler) - Dead project that is rule-based.
- [pyrules](https://github.com/miraculixx/pyrules) - Dead project that supports rule based corrections (but no validation).

## Similar work (R)

This project is inspired by https://github.com/data-cleaning/.
Similar functionality can be found in the following R packages:

- [validate](https://github.com/data-cleaning/validate) - Checking data (implemented)
- [dcmodify](https://github.com/data-cleaning/dcmodify) - Correcting data (implemented)
- [errorlocate](https://github.com/data-cleaning/errorlocate) - Identifying and removing errors (not yet implemented)
- [deductive](https://github.com/data-cleaning/deductive) - Deductivate correction based on checks (not yet implemented)

Features found in one of the packages above but not implemented here, might eventually make it into this package too.
