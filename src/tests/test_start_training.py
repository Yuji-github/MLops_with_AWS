from start_training import _import_csv
from unittest import TestCase
import unittest.mock as mock
import pandas as pd
import unittest


class TestStartTraining(TestCase):
    def test_import_csv(self):
        """Testing _import_csv
        return type is pandas.DataFrame
        read_csv called with "test"
        the return dataframe has the same value that is mocked
        """
        mock_df = pd.DataFrame({"data": [1]})

        with mock.patch("pandas.read_csv") as read_csv_mock:
            read_csv_mock.return_value = mock_df
            test_result = _import_csv("test")

        self.assertEqual(type(test_result), pd.DataFrame)
        read_csv_mock.assert_called_once_with("test")
        pd.testing.assert_frame_equal(mock_df, test_result, check_dtype=False)


if __name__ == "__main__":
    unittest.main()
