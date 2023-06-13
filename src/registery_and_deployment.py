import boto3
import os
import argparse
from urllib.parse import urlparse
from typing import Tuple


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_folder_name_s3", type=str, default=None, help="folder path for s3")
    parser.add_argument("--folder", type=str, default="download", help="saving files to the folder from s3")

    return parser.parse_args()


def download_s3(model_folder_name_s3: str, folder: str):
    """Downloading files from s3 bucket folder

    :param model_folder_name_s3:
    :param folder:
    :return:

    e.g.
    model_folder_name_s3 = s3://s3-bucket-name/1234/5678/artifacts/GradientBoost
    folder = download
    """

    def separate_path(model_folder_name_s3: str) -> Tuple[str, str]:
        """Separating into bucket and path

        :param model_folder_name_s3:
             s3://s3-bucket-name/1234/5678/artifacts/GradientBoost

        :return bucket_name,bucket_prefix:
            s3-bucket-name, /1234/5678/artifacts/GradientBoost
        """
        parse_object = urlparse(model_folder_name_s3)
        bucket_name = parse_object.netloc
        bucket_prefix = parse_object.path[1:]
        return bucket_name, bucket_prefix

    bucket_name, bucket_prefix = separate_path(model_folder_name_s3)

    if not os.path.exists(folder):
        os.mkdir(folder)
        os.chdir(folder)
        print("Folder %s created!" % folder)
    else:
        os.chdir(folder)

    cur_path = os.getcwd()
    client_s3 = boto3.client("s3")  # boto3.client(service_name): The name of a service, e.g. 's3' or 'ec2'.
    list_s3 = client_s3.list_objects_v2(
        Bucket=bucket_name, Prefix=bucket_prefix
    )  # Bucket is s3 bucket name. Prefix is Limits the response to keys that begin with the specified prefix.

    for obj in list_s3["Contents"]:

        try:
            filename = obj["Key"].rsplit("/", 1)[1]
        except IndexError:
            filename = obj["Key"]

        localfilename = os.path.join(cur_path, filename)
        client_s3.download_file(bucket_name, obj["Key"], localfilename)


if __name__ == "__main__":
    args = parse_args()
    download_s3(args.model_folder_name_s3, args.folder)
