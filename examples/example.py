import pandas as pd

from datarules import CheckList, CorrectionList, Context

pd.set_option('display.max_columns', None)

df = pd.DataFrame([
    {"width": 3, "height": 7},
    {"width": 3, "height": 5, "depth": 1},
    {"width": 3, "height": 8},
    {"width": 3, "height": 3},
    {"width": 3, "height": -2, "depth": 4},
])

# This ensures NA becomes a valid value.
df['depth'] = df['depth'].convert_dtypes(convert_integer=False)

# Option 1: Rules in python
checks = CheckList.from_file('rules/checks.py')
corrections = CorrectionList.from_file('rules/corrections.py')

# Option 2: Rules in yaml-format
# checks = CheckList.from_file('rules/checks.yaml')
# corrections = CorrectionList.from_file('rules/corrections.yaml')

# Context can be used to add static parameters
# If using yaml, this is also used to import modules.
context = Context({'year': 2024})
context.add_module("numpy", alias='np')


def main():
    check_report = checks.run(df)
    correction_report = corrections.run(df, context)

    print("Check report")
    print(check_report.summary())
    print()
    print("Correction report")
    print(correction_report.summary())
    print()
    print("Corrected data")
    print(df)


if __name__ == "__main__":
    main()
