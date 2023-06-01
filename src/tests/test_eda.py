from unittest import TestCase
import pandas as pd
import numpy as np
from eda import EDA
import unittest


class TestEDA(TestCase):
    def setUp(self):
        df = pd.DataFrame({"test": [1]})
        self.eda = EDA(df)

    def test_check_missing_data_return_False(self):
        """Testing _check_missing_data

        :except: False
        """
        self.assertEqual(self.eda._check_missing_data(), False)

    def test_check_missing_data_return_True(self):
        """Testing _check_missing_data

        :except: True
        because of the missing values
        """

        missing_df = pd.DataFrame({"test": [1, 2], "miss": [np.nan, np.nan]})
        self.eda.df = missing_df
        self.assertEqual(self.eda._check_missing_data(), True)

    def test_replace_df_cols(self):
        """Testing _replace_df_cols

        :except: data frame that is replaced by int
        """
        exp_df = pd.DataFrame({"Color": [1, 3, 3, 2, 2, 4, 4, 0, 3], "Spectral_Class": [0, 1, 2, 3, 4, 5, 6, 5, 0]})

        df = pd.DataFrame(
            {
                "Color": [
                    "Blue-White",
                    "yellowish",
                    "Yellowish White",
                    "White",
                    "Whitish",
                    "Orange-Red",
                    "Pale yellow orange",
                    "Red",
                    "white-Yellow",
                ],
                "Spectral_Class": ["M", "B", "A", "F", "O", "K", "G", "K", "M"],
            }
        )
        self.eda.df = df
        self.eda._replace_df_cols()

        pd.testing.assert_frame_equal(exp_df, self.eda.df, check_dtype=False)

    def test_spread_df(self):
        """Testing _spread_df

        :except: 4 np.arrays and each return has different shapes
        """
        df = pd.DataFrame({"Color": [1, 2, 3, 4, 5], "Spectral_Class": [1, 2, 3, 4, 5], "Type": [1, 2, 3, 4, 5]})

        self.eda.df = df
        x_train, x_test, y_train, y_test = self.eda._spread_df()
        self.assertEqual((4, 2), x_train.shape)
        self.assertEqual((1, 2), x_test.shape)
        self.assertEqual((4,), y_train.shape)
        self.assertEqual((1,), y_test.shape)


if __name__ == "__main__":
    unittest.main()
