from unittest import TestCase

import pandas as pd
import numpy as np

from pymodify import check, run_checks, Check


@check
def check_almost_square(width, height):
    return (width - height).abs() < 5


@check
def check_width_around_3(width):
    return np.allclose(width, 3)


@check
def check_not_too_deep(depth):
    return depth < 3


check_trivial = Check("width < height or width == height or width > height",
                      name="check_trivial")


checklist = [
    check_almost_square,
    check_width_around_3,
    check_not_too_deep,
    check_trivial,
]


class CheckTests(TestCase):
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

    def test_check(self):
        check_result = check_almost_square.run(self.df)
        self.assertEqual(5, check_result.items)
        self.assertEqual(3, check_result.passes)
        self.assertEqual(2, check_result.fails)
        self.assertEqual(0, check_result.nas)
        self.assertEqual(None, check_result.error)
        self.assertEqual(False, check_result.has_error)
        self.assertEqual([], check_result.warnings)

    def test_check_whole(self):
        check_result = check_width_around_3.run(self.df)
        self.assertEqual(1, check_result.items)
        self.assertEqual(1, check_result.passes)
        self.assertEqual(0, check_result.fails)
        self.assertEqual(0, check_result.nas)
        self.assertEqual(None, check_result.error)
        self.assertEqual(False, check_result.has_error)
        self.assertEqual([], check_result.warnings)

    def test_check_depth(self):
        """Attribute which might be missing"""
        check_result = check_not_too_deep.run(self.df)
        self.assertEqual(5, check_result.items)
        self.assertEqual(1, check_result.passes)
        self.assertEqual(1, check_result.fails)
        self.assertEqual(3, check_result.nas)
        self.assertEqual(None, check_result.error)
        self.assertEqual(False, check_result.has_error)
        self.assertEqual([], check_result.warnings)

    def test_check_trivial(self):
        """Attribute which might be missing"""
        check_result = check_trivial.run(self.df)
        print("check_result = {!r}".format(check_result))
        self.assertEqual(5, check_result.items)
        self.assertEqual(5, check_result.passes)
        self.assertEqual(0, check_result.fails)
        self.assertEqual(0, check_result.nas)
        self.assertEqual(None, check_result.error)
        self.assertEqual(False, check_result.has_error)
        self.assertEqual([], check_result.warnings)

    def test_check_together(self):
        check_report = run_checks(self.df, checklist)
        summary = check_report.summary()
        dataframe = check_report.dataframe()

        expected_summary = [
            {'name': 'check_almost_square',
             'condition': 'check_almost_square(width, height)',
             'items': 5,
             'passes': 3,
             'fails': 2,
             'NAs': 0,
             'error': None,
             'warnings': 0},
            {'name': 'check_width_around_3',
             'condition': 'check_width_around_3(width)',
             'items': 1,
             'passes': 1,
             'fails': 0,
             'NAs': 0,
             'error': None,
             'warnings': 0},
            {'name': 'check_not_too_deep',
             'condition': 'check_not_too_deep(depth)',
             'items': 5,
             'passes': 1,
             'fails': 1,
             'NAs': 3,
             'error': None,
             'warnings': 0},
            {'name': 'check_trivial',
             'condition': '(width < height) | (width == height) | (width > height)',
             'items': 5,
             'passes': 5,
             'fails': 0,
             'NAs': 0,
             'error': None,
             'warnings': 0},
        ]

        expected_df = [
            {'check_almost_square': True,
             'check_width_around_3': True,
             'check_not_too_deep': None,
             'check_trivial': True},
            {'check_almost_square': True,
             'check_width_around_3': True,
             'check_not_too_deep': True,
             'check_trivial': True},
            {'check_almost_square': False,
             'check_width_around_3': True,
             'check_not_too_deep': None,
             'check_trivial': True},
            {'check_almost_square': True,
             'check_width_around_3': True,
             'check_not_too_deep': None,
             'check_trivial': True},
            {'check_almost_square': False,
             'check_width_around_3': True,
             'check_not_too_deep': False,
             'check_trivial': True}]

        self.assertEqual(expected_summary, summary.to_dict('records'))
        self.assertEqual(expected_df, dataframe.to_dict('records'))
