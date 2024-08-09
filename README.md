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

1) Checks (if data is correct). Also knows as validations.
2) Corrections (how to fix incorrect data).

## Example

Create some data
```python
import pandas as pd

df = pd.DataFrame([
    {"width": 3, "height": 7},
    {"width": 3, "height": 8},
])
```

1. Check the data
```python
from datarules import CheckList, Check
from uneval import quote as q

checks = CheckList([
    Check(name="almost_square",
          tags=["low-priority"],
          test=(q.width - q.height).abs() <= 4),
])
check_report = checks.run(df)
print(check_report)
```

Output:
```
CheckReport
-----------
          name                         test  items  passes  fails  NAs error  warnings
 almost_square  (width - height).abs() <= 4      2       1      1    0  None         0
```

2. Correct the data
```python
from datarules import CorrectionList, Correction

corrections = CorrectionList([
    Correction(name="correct_square",
               trigger=checks[0].fails,
               action={"height": q.height / 2 + q.width / 2}),
])
correction_report = corrections.run(df)
print(correction_report)
print(f"Modified data:\n{df}")
```

Output:
```
CorrectionReport
----------------
           name                             trigger                           action  applied error  warnings
 correct_square  almost_square.fails(height, width)  height = height / 2 + width / 2        1  None         0

Modified data:
   width  height
0      3     7.0
1      3     5.5
```

See more examples on [DataRules examples](https://github.com/lverweijen/datarules/tree/main/examples).

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
- [deductive](https://github.com/data-cleaning/deductive) - Deductive correction based on checks (not yet implemented)
