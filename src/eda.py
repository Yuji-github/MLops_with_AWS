import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from typing import Tuple


class EDA:
    """EDA (Exploratory Data Analysis)
    Analyzing data sets (Not logging this part)

    Attributes:
        df: pd.DataFrame
        sc: StandardScaler
    """

    def __init__(self, df: pd.DataFrame):
        self.df: pd.DataFrame = df
        self.sc: StandardScaler

    def _check_missing_data(self) -> bool:
        """Checking missing values

        :return: bool
        """
        missing_values: pd.Series = self.df.isnull().sum()
        return False if missing_values.sum() == 0 else True

    def _replace_df_cols(self) -> None:
        """replace the Color and Spectral_Class columns with int

        :return: None
        """

        # replace Color col
        self.df.replace({"Blue-White": "Blue-white"}, regex=True, inplace=True)
        self.df.replace({"Blue White": "Blue-white"}, regex=True, inplace=True)
        self.df.replace({"Blue white": "Blue-white"}, regex=True, inplace=True)
        self.df.replace({"yellowish": "yellow-white"}, regex=True, inplace=True)
        self.df.replace({"Yellowish": "yellow-white"}, regex=True, inplace=True)
        self.df.replace({"Yellowish White": "yellow-white"}, regex=True, inplace=True)
        self.df.replace({"White": "white"}, regex=True, inplace=True)
        self.df.replace({"Whitish": "white"}, regex=True, inplace=True)
        self.df.replace({"Orange-Red": "Orange"}, regex=True, inplace=True)
        self.df.replace({"Pale yellow orange": "Orange"}, regex=True, inplace=True)
        self.df.replace({"yellow-white white": "yellow-white"}, regex=True, inplace=True)
        self.df.replace({"white-Yellow": "yellow-white"}, regex=True, inplace=True)

        replace_dict = {"Red": 0, "Blue-white": 1, "white": 2, "yellow-white": 3, "Orange": 4, "Blue": 5}
        self.df.Color.replace(replace_dict, inplace=True)

        # replace Spectral_Class col
        replace_dict = {"M": 0, "B": 1, "A": 2, "F": 3, "O": 4, "K": 5, "G": 6}
        self.df.Spectral_Class.replace(replace_dict, inplace=True)

    def _spread_df(self) -> Tuple[np.array, np.array, np.array, np.array]:
        """Spreading data sets with transform function

        :return: np.array, np.array, np.array, np.array
        """

        x, y = self.df.iloc[:, :-1], self.df.iloc[:, -1]
        self.sc = StandardScaler()

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        x_train = self.sc.fit_transform(x_train)
        x_test = self.sc.transform(x_test)

        return x_train, x_test, y_train, y_test
