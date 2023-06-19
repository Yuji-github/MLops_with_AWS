import pandas as pd
import json
import boto3
from eda import EDA
import argparse
import random


def check_status(endpoint_name: str, region: str) -> str:
    """Checking status of sagemaker
    InService means running the endpoint

    :param endpoint_name:
    :param region:
    :return str:
    """
    sage_client = boto3.client("sagemaker", region_name=region)
    endpoint_description = sage_client.describe_endpoint(EndpointName=endpoint_name)
    endpoint_status = endpoint_description["EndpointStatus"]
    return endpoint_status


def parse_args() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint_name", type=str, default=None, help="EndPoint Name on Sagemaker")
    parser.add_argument("--region", type=str, default="ap-southeast-2", help="Region where in Service")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # check endpoint status
    if check_status(args.endpoint_name, args.region) == "InService":

        # Prepare data to give for predictions
        df = pd.read_csv("src/Stars.csv")
        this_eda = EDA(df)
        this_eda._replace_df_cols()
        x_train, x_test, y_train, y_test = this_eda._spread_df()

        # selecting test data
        test_idx = random.randrange(len(x_test))  # getting random number from the range
        data = {"instances": [x_test[test_idx].tolist()]}  # need to be 2D array

        # connecting Sagemaker
        client = boto3.client("sagemaker-runtime")

        # Body and ContentType must be same
        # invoke_endpoint predicts the results with given values (Body)
        # reference: https://medium.com/ml-bytes/how-to-make-predictions-against-a-sagemaker-endpoint-using-tensorflow-serving-8b423b9b316a

        response = client.invoke_endpoint(
            EndpointName=args.endpoint_name, Body=json.dumps(data), ContentType="application/json"
        )

        # decoding (converting) the response
        preds = response["Body"].read().decode("ascii")
        preds = json.loads(preds)
        print(f"Received response: {preds}, actual {y_test.iloc[test_idx]}")
