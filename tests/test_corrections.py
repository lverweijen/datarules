from unittest import TestCase

import pandas as pd

from datarules import check, correction, CorrectionList


@check
def check_almost_square(width, height):
    return (width - height).abs() < 5


@correction(trigger=check_almost_square.fails)
def make_square(width, height):
    return {"height": height + (width - height) / 2}


correctionlist = CorrectionList([make_square])


class CorrectionTests(TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {"width": 3, "height": 7},
            {"width": 3, "height": 5, "depth": 1},
            {"width": 3, "height": 8},
            {"width": 3, "height": 3},
            {"width": 3, "height": -2, "depth": 4},
        ])

        # Make depth nullable
        self.df['depth'] = self.df['depth'].convert_dtypes()

    def test_correction(self):
        df = self.df.copy()
        result = make_square.run(df)
        self.assertEqual("make_square", str(result.correction.name))
        self.assertEqual("check_almost_square.fails(width, height)", str(result.correction.trigger))
        self.assertEqual("make_square(width, height)", str(result.correction.action))
        self.assertEqual(2, result.applied.sum())
        self.assertEqual(None, result.error)
        self.assertEqual(0, len(result.warnings))

    def test_corrections_together(self):
        check_report = correctionlist.run(self.df)
        summary = check_report.summary()
        dataframe = check_report.dataframe()

        expected_summary = [
            {'name': 'make_square',
             'trigger': 'check_almost_square.fails(width, height)',
             'action': 'make_square(width, height)',
             'applied': 2,
             'error': None,
             'warnings': 0}
        ]

        expected_dataframe = [
            {"make_square": False},
            {"make_square": False},
            {"make_square": True},
            {"make_square": False},
            {"make_square": True},
        ]

        self.assertEqual(expected_summary, summary.to_dict('records'))
        self.assertEqual(expected_dataframe, dataframe.to_dict('records'))
