import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets
import json
import boto3
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from eda import EDA

global app_name
global region

app_name = "sagemaker-model"  # model name on sagemaker
region = "ap-southeast-2"


def check_status(app_name: str):
    sage_client = boto3.client("sagemaker", region_name=region)
    endpoint_description = sage_client.describe_endpoint(EndpointName=app_name)
    endpoint_status = endpoint_description["EndpointStatus"]
    return endpoint_status


def query_endpoint(app_name: str, input_json):
    client = boto3.session.Session().client("sagemaker-runtime", region)

    response = client.invoke_endpoint(
        EndpointName=app_name,
        Body=input_json,
        ContentType="application/json; format=pandas-split",
    )
    print(response)
    preds = response["Body"].read().decode("ascii")
    preds = json.loads(preds)
    print("Received response: {}".format(preds))
    return preds


## check endpoint status
print("Application status is: {}".format(check_status(app_name)))

# Prepare data to give for predictions
df = pd.read_csv("src/Stars.csv")

this_eda = EDA(df)
this_eda._replace_df_cols()
x_train, x_test, y_train, y_test = this_eda._spread_df()


# ## create test data and make inference from enpoint
query_input = pd.DataFrame(x_test).iloc[[3]].to_json(orient="split")
print(query_input)
# prediction = query_endpoint(app_name=app_name, input_json=query_input)
