import pandas as pd
from pymodify import load_checks, load_corrections, Runner

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
checks = load_checks('rules/checks.py')
corrections = load_corrections('rules/corrections.py')

# Option 2: Rules in yaml-format
# checks = load_checks('rules/checks.yaml')
# corrections = load_corrections('rules/corrections.yaml')


def main():
    runner = Runner()
    check_report = runner.check(df, checks)
    correction_report = runner.correct(df, corrections)

    pd.set_option('display.max_columns', None)

    print("Check report")
    print(check_report.summary())
    print()
    print("Correction report")
    print(correction_report.summary())
    print()
    print("Corrected data")
    print(df)

    with open('check_report.txt', 'w') as fp:
        fp.write(check_report.summary().to_string())
    with open('correction_report.txt', 'w') as fp:
        fp.write(correction_report.summary().to_string())


if __name__ == "__main__":
    main()
