import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from analyze_spills import load_data, clean_data, aggregate_data

class TestAnalyzeSpills(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_load_data(self, mock_read_csv):
        mock_df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
        mock_read_csv.return_value = mock_df
        data = load_data('dummy_path.csv')
        pd.testing.assert_frame_equal(data, mock_df)
        mock_read_csv.assert_called_once_with('dummy_path.csv')

    def test_clean_data(self):
        input_df = pd.DataFrame({'category': ['A', 'A', 'B'], 'total': [1, 1, None]})
        # Expected behavior: dropna removes the row with None, drop_duplicates removes the duplicate row
        cleaned_data = clean_data(input_df)
        self.assertEqual(len(cleaned_data), 1)
        self.assertEqual(cleaned_data.iloc[0]['category'], 'A')
        self.assertEqual(cleaned_data.iloc[0]['total'], 1)

    def test_aggregate_data(self):
        input_df = pd.DataFrame({'category': ['A', 'A', 'B'], 'total': [1, 2, 4]})
        aggregated = aggregate_data(input_df)
        self.assertEqual(len(aggregated), 2)
        self.assertEqual(aggregated[aggregated['category'] == 'A']['total'].values[0], 3)
        self.assertEqual(aggregated[aggregated['category'] == 'B']['total'].values[0], 4)

if __name__ == '__main__':
    unittest.main()
