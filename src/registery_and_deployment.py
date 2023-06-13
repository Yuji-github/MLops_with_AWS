import boto3
import os


def download_s3(BUCKET_NAME, BUCKET_PREFIX):
    """Create a low-level service client by name using the default session.

    :param service_name: The name of a service, e.g. 's3' or 'ec2'. You
            can get a list of available services via
    """

    # BUCKET_NAME = "mlflow-s3-bucket-1"
    # BUCKET_PREFIX = "584097635432506948/0153458fb9fa45c7b560f9f9fbbae162/artifacts/GradientBoost"

    if not os.path.exists(File_name):
        os.mkdir(File_name)
        os.chdir(File_name)
        print("Folder %s created!" % File_name)
    else:
        os.chdir(File_name)

    cur_path = os.getcwd()
    client_s3 = boto3.client("s3")
    list_s3 = client_s3.list_objects_v2(
        Bucket=BUCKET_NAME, Prefix=BUCKET_PREFIX
    )  # Bucket is s3 bucket name. Prefix is Limits the response to keys that begin with the specified prefix.

    for obj in list_s3["Contents"]:

        try:
            filename = obj["Key"].rsplit("/", 1)[1]
        except IndexError:
            filename = obj["Key"]

        localfilename = os.path.join(cur_path, filename)
        client_s3.download_file(BUCKET_NAME, obj["Key"], localfilename)


if __name__ == "__main__":
    BUCKET_NAME = input("Enter bucket name:")
    BUCKET_PREFIX = input("Enter s3 folder/files:")
    File_name = input("Enter the download files:")
    if not os.path.exists(File_name):
        os.mkdir(File_name)
        os.chdir(File_name)
        print("Folder %s created!" % File_name)
    else:
        os.chdir(File_name)

    download_s3(BUCKET_NAME, BUCKET_PREFIX)
