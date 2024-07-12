from unittest import TestCase

from datarules.utilities import toposort

import datarules as dr


class TestUtilities(TestCase):
    def test_toposort(self):
        actions = dr.CorrectionList([
            dr.Correction("f = x", name="f"),
            dr.Correction("z, x = b - c", name="zx"),
            dr.Correction("b = a * a", name="b"),
            dr.Correction("c = a - b", name="c"),
            dr.Correction("d = c - b", name="d"),
            dr.Correction("a = 9", name="a"),
        ])
        results = [c.name for c in toposort(actions)]
        expected = ["a", "b", "c", "zx", "d", "f"]
        self.assertEqual(expected, results)
