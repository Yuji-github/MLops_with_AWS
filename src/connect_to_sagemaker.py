import pandas as pd
import json
import boto3
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


# def query_endpoint(app_name: str, input_json):
#     # client = boto3.session.Session().client("sagemaker-runtime", region)
#     client = boto3.client('sagemaker-runtime')
#     response = client.invoke_endpoint(
#         EndpointName=app_name,
#         Body=input_json,
#         ContentType="application/json; format=pandas-split",
#     )
#     print(response)
#     preds = response["Body"].read().decode("ascii")
#     preds = json.loads(preds)
#     print("Received response: {}".format(preds))
#     return None


## check endpoint status
print("Application status is: {}".format(check_status(app_name)))

# Prepare data to give for predictions
df = pd.read_csv("src/Stars.csv")

this_eda = EDA(df)
this_eda._replace_df_cols()
x_train, x_test, y_train, y_test = this_eda._spread_df()

actual = y_test.iloc[3]
# ## create test data and make inference from enpoint
data = {"instances": [x_test[3].tolist()]}  # need to be 2D array

print(data)

client = boto3.client("sagemaker-runtime")

# Body and ContentType must be same
# invoke_endpoint predicts the results with given values (Body)
response = client.invoke_endpoint(EndpointName=app_name, Body=json.dumps(data), ContentType="application/json")

# decoding (converting) the response
preds = response["Body"].read().decode("ascii")
preds = json.loads(preds)
print(f"Received response: {preds}, actual {actual}")
