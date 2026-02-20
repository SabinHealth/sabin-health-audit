import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from analyze_encampments_311 import (
    aggregate_monthly,
    build_chart,
    filter_encampments,
    load_data,
    main,
    save_csv,
)


class TestAnalyzeEncampments311(unittest.TestCase):

    @patch('analyze_encampments_311.pd.read_csv')
    def test_load_data(self, mock_read_csv):
        mock_data = pd.DataFrame({'Case Summary': ['Encampment Reporting'], 'Case Created Date': ['2025-01-15']})
        mock_read_csv.return_value = mock_data
        data = load_data('dummy_path.csv')
        pd.testing.assert_frame_equal(data, mock_data)
        mock_read_csv.assert_called_once_with('dummy_path.csv')

    @patch('analyze_encampments_311.pd.read_csv')
    def test_load_data_file_not_found(self, mock_read_csv):
        mock_read_csv.side_effect = FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            load_data('missing.csv')

    def test_filter_encampments(self):
        data = pd.DataFrame({
            'Case Summary': ['Encampment Reporting', 'Pothole', 'Sweep Request', 'Noise Complaint']
        })
        target = ['Encampment Reporting', 'Sweep Request']
        result = filter_encampments(data, target)
        self.assertEqual(len(result), 2)
        self.assertTrue(result['Case Summary'].isin(target).all())

    def test_aggregate_monthly(self):
        data = pd.DataFrame({
            'Case Created Date': ['2025-01-10', '2025-01-20', '2025-02-05'],
            'Case Summary': ['Encampment Reporting', 'Sweep Request', 'Encampment Reporting']
        })
        result = aggregate_monthly(data)
        self.assertIn('YearMonth', result.columns)
        self.assertIn('Encampment_Reports', result.columns)
        self.assertEqual(result['Encampment_Reports'].sum(), 3)

    def test_aggregate_monthly_drops_invalid_dates(self):
        data = pd.DataFrame({
            'Case Created Date': ['2025-01-10', None, '2025-02-05'],
            'Case Summary': ['Encampment Reporting', 'Sweep Request', 'Encampment Reporting']
        })
        result = aggregate_monthly(data)
        self.assertEqual(result['Encampment_Reports'].sum(), 2)

    @patch('analyze_encampments_311.pd.DataFrame.to_csv')
    def test_save_csv(self, mock_to_csv):
        data = pd.DataFrame({'YearMonth': ['2025-01'], 'Encampment_Reports': [5]})
        save_csv(data, 'output.csv')
        mock_to_csv.assert_called_once_with('output.csv', index=False)

    @patch('analyze_encampments_311.plt')
    def test_build_chart(self, mock_plt):
        monthly_counts = pd.DataFrame({
            'YearMonth': pd.period_range('2025-01', periods=3, freq='M'),
            'Encampment_Reports': [10, 15, 8]
        })
        build_chart(monthly_counts, '2026-02', 'output.png', 'Test Title')
        mock_plt.savefig.assert_called_once()

    @patch('analyze_encampments_311.build_chart')
    @patch('analyze_encampments_311.save_csv')
    @patch('analyze_encampments_311.aggregate_monthly')
    @patch('analyze_encampments_311.filter_encampments')
    @patch('analyze_encampments_311.load_data')
    def test_main(self, mock_load, mock_filter, mock_aggregate, mock_save, mock_chart):
        mock_load.return_value = MagicMock()
        mock_filter.return_value = MagicMock()
        mock_aggregate.return_value = MagicMock()
        main()
        mock_load.assert_called_once()
        mock_filter.assert_called_once()
        mock_aggregate.assert_called_once()
        mock_save.assert_called_once()
        mock_chart.assert_called_once()


if __name__ == '__main__':
    unittest.main()
