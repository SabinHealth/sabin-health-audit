import unittest
from compare_ozone import compare_ozone
from config import FEDERAL_OZONE_LIMIT

class TestCompareOzone(unittest.TestCase):

    def test_comparison(self):
        data = [
            {'id': 1, 'ozone_level': FEDERAL_OZONE_LIMIT - 0.01},
            {'id': 2, 'ozone_level': FEDERAL_OZONE_LIMIT + 0.01},
            {'id': 3, 'description': 'missing ozone_level'}
        ]
        result = compare_ozone(data)

        expected = {
            1: 'Within safe levels',
            2: 'Exceeds allowable level'
        }
        self.assertEqual(result, expected)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            compare_ozone("not a list")

if __name__ == '__main__':
    unittest.main()
