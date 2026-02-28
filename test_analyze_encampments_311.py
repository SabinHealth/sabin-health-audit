import unittest
from unittest.mock import patch
import pandas as pd
from analyze_encampments_311 import clean_data, aggregate_data
from config import ENCAMPMENTS_TARGET_SUMMARIES

class TestAnalyzeEncampments(unittest.TestCase):

    def test_clean_data(self):
        data = {
            'Case Summary': [ENCAMPMENTS_TARGET_SUMMARIES[0], 'Other', ENCAMPMENTS_TARGET_SUMMARIES[1]],
            'Case Created Date': ['2025-01-01', '2025-01-02', '2025-02-01']
        }
        df = pd.DataFrame(data)
        cleaned_df = clean_data(df)

        self.assertEqual(len(cleaned_df), 2)
        self.assertTrue(all(cleaned_df['Case Summary'].isin(ENCAMPMENTS_TARGET_SUMMARIES)))
        self.assertEqual(cleaned_df['YearMonth'].iloc[0], pd.Period('2025-01', freq='M'))

    def test_aggregate_data(self):
        data = {
            'YearMonth': [pd.Period('2025-01', freq='M'), pd.Period('2025-01', freq='M'), pd.Period('2025-02', freq='M')],
            'Case Summary': ['A', 'A', 'A'] # values don't matter for size()
        }
        df = pd.DataFrame(data)
        # Mock to_csv to avoid creating file
        with patch('pandas.DataFrame.to_csv'):
            aggregated = aggregate_data(df)

        self.assertEqual(len(aggregated), 2)
        self.assertEqual(aggregated[aggregated['YearMonth'] == '2025-01']['Encampment_Reports'].values[0], 2)
        self.assertEqual(aggregated[aggregated['YearMonth'] == '2025-02']['Encampment_Reports'].values[0], 1)

if __name__ == '__main__':
    unittest.main()
