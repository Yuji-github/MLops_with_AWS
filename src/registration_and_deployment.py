"""Entry point to run the code
Step 1: (this runs at start_training.py)
    EDA (Exploratory Data Analysis)
Step 2: (this runs at start_training.py)
    Create a model : Save the artifacts on S3
Step 3: (this runs at start_training.py)
    Evaluate the model : Save the artifacts on S3
Step 4:
    Deploy the model : Save the artifacts on Sagemaker
    *Make sure your Docker Desktop is running while running
Step 5:
    Test deployment
"""

import boto3
import argparse
from urllib.parse import urlparse
from typing import Tuple
from deploy import create_simple_dict_for_sagemaker, deploy_model_to_sagemaker
import subprocess
import json
import os
import docker


def parse_args() -> argparse:
    parser = argparse.ArgumentParser()
    parser.add_argument("--windows", "-w", type=eval, choices=[True, False], default=True, help="windows or others")

    # registry to ECR
    parser.add_argument(
        "--registry_image_ecr",
        "-ri",
        type=eval,
        choices=[True, False],
        default=True,
        help="registry image on ECR",
    )
    parser.add_argument(
        "--folder_name_s3",
        "-fs3",
        type=str,
        default=None,
        help="folder that contains best model from s3 bucket",
    )
    parser.add_argument(
        "--folder", "-f", type=str, default="download", help="saving files to the folder from s3 bucket"
    )
    parser.add_argument("--local_folder_path", "-lfp", type=str, default=None, help="selecting local folder path")
    parser.add_argument(
        "--model_name_for_ECR", "-mne", type=str, default="latest-model-ecr", help="model name for registry on ECR"
    )

    # deployment on Sagemaker
    parser.add_argument(
        "--deployment",
        "-d",
        type=eval,
        choices=[True, False],
        default=False,
        help="if true, then, it deploys the model to sagemaker",
    )
    parser.add_argument(
        "--model_name_for_Sagemaker",
        "-mns",
        type=str,
        default="latest-model-sagemaker",
        help="model name for deployment on sagemaker",
    )

    # simple config for deployment on Sagemaker
    parser.add_argument(
        "--create_config",
        "-cc",
        type=eval,
        choices=[True, False],
        default=False,
        help="create a simple config dict to push the image to sagemaker",
    )
    parser.add_argument(
        "--dict_config", "-dc", type=json.loads, default=None, help="dict config for pushing image to sagemaker"
    )
    parser.add_argument(
        "--execution_role_arn",
        "-arn",
        type=str,
        default=None,
        help="execution_role_arn: get the value from AWS->IAM->Roles",
    )
    parser.add_argument(
        "--bucket_name_for_sagemaker", "-bn", type=str, default=None, help="bucket name for deployment on sagemaker"
    )
    parser.add_argument("--image_url_ecr", "-iu", type=str, default=None, help="image url on ECR")
    parser.add_argument("--region_name", "-rn", type=str, default=None, help="region name for sagemaker")
    parser.add_argument(
        "--instance_type",
        "-it",
        type=str,
        default=None,
        help="instance type for sagemaker: https://aws.amazon.com/sagemaker/pricing/",
    )
    parser.add_argument("--instance_count", "-ic", type=int, default=1, help="instance count for sagemaker")

    return parser.parse_args()


def download_s3(folder_name_s3: str, folder: str) -> str:
    """Downloading files from s3 bucket folder

    :param folder_name_s3:
    :param folder:
    :return:

    e.g.
    model_folder_name_s3 = s3://s3-bucket-name/1234/5678/artifacts/GradientBoost
    folder = download
    """

    def separate_path(folder_name_s3: str) -> Tuple[str, str]:
        """Separating into bucket and path

        :param folder_name_s3:
             s3://s3-bucket-name/1234/5678/artifacts/GradientBoost

        :return bucket_name,bucket_prefix:
            s3-bucket-name, /1234/5678/artifacts/GradientBoost
        """
        parse_object = urlparse(folder_name_s3)
        bucket_name = parse_object.netloc
        bucket_prefix = parse_object.path[1:]
        return bucket_name, bucket_prefix

    bucket_name, bucket_prefix = separate_path(folder_name_s3)

    if not os.path.exists(folder):
        os.mkdir(folder)
        print("Folder %s created!" % folder)

    saving_path = os.path.join(os.getcwd(), folder)
    client_s3 = boto3.client("s3")  # boto3.client(service_name): The name of a service, e.g. 's3' or 'ec2'.
    list_s3 = client_s3.list_objects_v2(
        Bucket=bucket_name, Prefix=bucket_prefix
    )  # Bucket is s3 bucket name. Prefix is Limits the response to keys that begin with the specified prefix.

    for obj in list_s3["Contents"]:

        try:
            filename = obj["Key"].rsplit("/", 1)[1]
        except IndexError:
            filename = obj["Key"]

        localfilename = os.path.join(saving_path, filename)
        client_s3.download_file(bucket_name, obj["Key"], localfilename)

    return saving_path


if __name__ == "__main__":
    args = parse_args()

    # registration image to ECR
    if args.registry_image_ecr:
        model_uri_local_folder = download_s3(args.folder_name_s3, args.folder)

        with open("registry.sh", "w") as f:  # create a folder at this dir
            if args.windows:
                model_uri_local_folder = model_uri_local_folder.replace(
                    "\\", "/"
                )  # bash file does not work with slash on Windows

            f.write(f"cd {model_uri_local_folder}" + "\n")  # change the dir
            f.write(
                f"mlflow sagemaker build-and-push-container --build --push -c {args.model_name_for_ECR}"
            )  # push the image to ECR
        f.close()

        # running the registry.sh
        subprocess.call(
            ["bash", "registry.sh"], shell=True, env=os.environ.copy()
        )  # env=os.environ.copy() -> copying virtual env
    else:
        model_uri_local_folder = args.local_folder_path

    # deployment to Sagemaker
    if args.deployment:

        # get image tag from Docker (local) as the tag is same as on ECR
        docker_client = docker.from_env()
        image_url_ecr_with_tag: str = ""  # to replace the value with the tag

        for image_tags in docker_client.images.list():
            if [image_tag for image_tag in image_tags.tags if args.image_url_ecr in image_tag]:
                image_url_ecr_with_tag = [
                    image_tag for image_tag in image_tags.tags if args.image_url_ecr in image_tag
                ][0]
                break

        if args.create_config:
            config = create_simple_dict_for_sagemaker(
                execution_role_arn=args.execution_role_arn,
                bucket=args.bucket_name_for_sagemaker,
                image_url_ecr=image_url_ecr_with_tag,
                region_name=args.region_name,
                instance_type=args.instance_type,
                instance_count=args.instance_count,
            )
        else:
            config = args.dict_config

        deploy_model_to_sagemaker(args.model_name_for_Sagemaker, model_uri_local_folder, config)
