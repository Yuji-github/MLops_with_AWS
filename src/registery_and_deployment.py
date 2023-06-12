import boto3
import botocore
import os


def client():
    """Create a low-level service client by name using the default session.

    :param service_name: The name of a service, e.g. 's3' or 'ec2'. You
            can get a list of available services via
    """

    BUCKET_NAME = "mlflow-s3-bucket-1"
    BUCKET_PREFIX = "584097635432506948/0153458fb9fa45c7b560f9f9fbbae162/artifacts/GradientBoost"

    client_s3 = boto3.client("s3")
    list_s3 = client_s3.list_objects_v2(
        Bucket=BUCKET_NAME, Prefix=BUCKET_PREFIX
    )  # Bucket is s3 bucket name. Prefix is Limits the response to keys that begin with the specified prefix.

    for obj in list_s3["Contents"]:

        try:
            filename = obj["Key"].rsplit("/", 1)[
                1
            ]  # If Filename --> /local/path/file.txt this step are get only this file "file.txt"
        except IndexError:
            filename = obj["Key"]

        localfilename = os.path.join("C:\\Users\\User\\PycharmProjects\\MLops_with_AWS\\download\\", filename)
        client_s3.download_file(BUCKET_NAME, obj["Key"], localfilename)
    client_s3.close()


if __name__ == "__main__":
    client()
