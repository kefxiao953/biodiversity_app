import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

class TestLoadData(unittest.TestCase):
    @patch('builtins.open', unittest.mock.mock_open(read_data="id\tname\n1\texample"))
    @patch('os.path.expanduser')
    @patch('pandas.read_csv')
    @patch('streamlit.session_state', new_callable=MagicMock)
    def test_load_data_not_present(self, mock_session_state, mock_read_csv, mock_expanduser):
        from functions import load_data
        mock_expanduser.return_value = './data/tortoise.tsv'
        mock_read_csv.return_value = pd.DataFrame({'id': [1], 'name': ['example']})
        load_data()
        self.assertTrue(hasattr(mock_session_state, 'df_tortise'))
        self.assertEqual(mock_session_state.df_tortise.iloc[0]['name'], 'example')

    @patch('streamlit.session_state', new_callable=lambda: {'df_tortise': pd.DataFrame({'id': [1], 'name': ['example']})})
    def test_load_data_already_present(self, mock_session_state):
        from functions import load_data
        load_data()
        self.assertTrue('df_tortise' in mock_session_state)

class TestGBIFData(unittest.TestCase):

    @patch('requests.get')
    def test_gbif_data_success(self, mock_get):
        from functions import gbif_data

        # Define what the mock should return when its json method is called.
        mock_get.return_value.json.return_value = {
            'results': [{'country': 'Test Country'}]
        }

        # Configure the mock to return a Response-like object
        mock_get.return_value.ok = True
        mock_get.return_value.status_code = 200

        result = gbif_data('Test Species', max_pages=1)

        # Check that the DataFrame is not empty
        self.assertFalse(result.empty, "The result should not be empty")

        # Now we assume result is a list of dictionaries for further assertions
        # If result is not empty, check the contents of the first item
        if not result.empty:
            first_record = result.iloc[0]  # Access the first record of the DataFrame
            self.assertIn('country', first_record, "First item in result should have a 'country' key")
            self.assertEqual(first_record['country'], 'Test Country', "The country should be 'Test Country'")




    @patch('requests.get')
    def test_gbif_data_failure(self, mock_get):
        from functions import gbif_data
        mock_get.return_value.status_code = 500
        result = gbif_data('Test Species', max_pages=1)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
