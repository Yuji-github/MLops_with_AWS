"""Entry point to run the code
Step 1:
    EDA (Exploratory Data Analysis)
Step 2:
    Create a model : Save the artifacts on S3
Step 3:
    Evaluate the model : Save the artifacts on S3
Step 4:
    Deploy the model : Save the artifacts on Sagemaker
Step 5:
    Test deployment
"""
from settings import URI
import pandas as pd


def _import_csv(filename: str) -> pd.DataFrame:
    """Import data set with given dir
    :param filename:
    :return:
        pd.Dataframe
    """
    return pd.read_csv(filename)


if __name__ == "__main__":
    df = _import_csv("src/Stars.csv")
