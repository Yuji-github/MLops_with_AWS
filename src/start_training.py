"""Entry point to run the code
Step 1:
    EDA (Exploratory Data Analysis)
Step 2:
    Create a model : Save the artifacts on S3
Step 3:
    Evaluate the model : Save the artifacts on S3
Step 4: (this runs at registration_and_deployment.py)
    Deploy the model : Save the artifacts on Sagemaker
Step 5: (this runs at registration_and_deployment.py)
    Test deployment
"""
import pandas as pd
from tqdm import tqdm
import logging
import mlflow
from sklearn.ensemble import GradientBoostingClassifier
import lightgbm as lgb
from mlflow.models.signature import infer_signature
import subprocess

from train import Train
from eda import EDA
from settings import TRACKING_SERVER_HOST


def _import_csv(filename: str) -> pd.DataFrame:
    """Import data set with given dir

    :param filename:
    :return pd.Dataframe:
    """
    return pd.read_csv(filename)


if __name__ == "__main__":
    try:
        subprocess.call(
            "access_ec2_and_run.sh", shell=True, timeout=10
        )  # accessing EC2 and running Mlflow from EC2, 10 sec later training runs
    except subprocess.TimeoutExpired:
        pass  # to go through the next steps

    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    mlflow_experiment = mlflow.set_experiment("Mlops-with-AWS")

    df = _import_csv("src/Stars.csv")
    this_eda = EDA(df)

    if this_eda._check_missing_data():
        logging.warning("Missing Data Detected")

    this_eda._replace_df_cols()
    x_train, x_test, y_train, y_test = this_eda._spread_df()

    models = [[GradientBoostingClassifier(), "GradientBoost"], [lgb.LGBMClassifier(), "lightGBM"]]
    train = Train(mlflow)

    for model in models:
        train.initialise_model(model)

        for learning_rate in tqdm(train.learning_rate_range):
            for n_estimators in tqdm(train.n_estimators_range, leave=False):
                for max_depth in tqdm(train.max_depth_range, leave=False):

                    with mlflow.start_run(experiment_id=mlflow_experiment.experiment_id, tags={"version": "v1"}):
                        y_pred = train._train(
                            x_train,
                            y_train,
                            x_test,
                            learning_rate=learning_rate,
                            n_estimators=n_estimators,
                            max_depth=max_depth,
                        )
                        signature = infer_signature(x_train, y_pred)  # specify input and output formats

                        accuracy = train._evaluate(y_test, y_pred)

                        train._logging_params_to_mlflow(
                            learning_rate=learning_rate, n_estimators=n_estimators, max_depth=max_depth
                        )
                        train._logging_eval_to_mlflow(accuracy)
                        train._logging_model_to_mlflow(signature)
