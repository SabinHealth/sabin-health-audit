import unittest
from unittest.mock import patch, MagicMock
from analyze_spills import load_data, clean_data, aggregate_data, main

class TestAnalyzeSpills(unittest.TestCase):

    @patch('analyze_spills.pd.read_csv')
    def test_load_data(self, mock_read_csv):
        mock_data = {'column1': [1, 2], 'column2': [3, 4]}
        mock_read_csv.return_value = mock_data
        data = load_data('dummy_path.csv')
        self.assertEqual(data, mock_data)
        mock_read_csv.assert_called_once_with('dummy_path.csv')

    @patch('analyze_spills.load_data')
    def test_clean_data(self, mock_load_data):
        mock_load_data.return_value = {'column1': [1, None, 2], 'column2': [3, 4, None]}
        cleaned_data = clean_data('dummy_path.csv')
        self.assertNotIn(None, cleaned_data['column1'])
        self.assertNotIn(None, cleaned_data['column2'])

    @patch('analyze_spills.clean_data')
    def test_aggregate_data(self, mock_clean_data):
        mock_clean_data.return_value = {'column1': [1, 2], 'column2': [3, 4]}
        aggregated = aggregate_data('dummy_path.csv')
        self.assertEqual(sum(aggregated['column1']), 3)
        self.assertEqual(sum(aggregated['column2']), 7)

    @patch('analyze_spills.aggregate_data')
    def test_main(self, mock_aggregate_data):
        mock_aggregate_data.return_value = {'column1': [1], 'column2': [3]}
        with patch('builtins.print') as mocked_print:
            main()
            mocked_print.assert_called_once_with("Aggregated Data:", mock_aggregate_data.return_value)

if __name__ == '__main__':
    unittest.main()