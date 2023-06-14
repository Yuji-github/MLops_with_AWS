import boto3
import os
import argparse
from urllib.parse import urlparse
from typing import Tuple
from deploy import create_simple_dict_for_sagemaker, deploy_model_to_sagemaker
import subprocess
import json


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--windows", "-w", type=bool, default=True, help="windows or others")

    # registry to ECR
    parser.add_argument(
        "--model_folder_name_s3", "-mf", type=str, default=None, help="folder path for s3 to create image to ECR"
    )
    parser.add_argument("--folder", "-f", type=str, default="download", help="saving files to the folder from s3")
    parser.add_argument(
        "--model_name_for_ECR", "-mne", type=str, default="latest-model-ecr", help="model name for registry on ECR"
    )

    # deployment on Sagemaker
    parser.add_argument(
        "--deployment", "-d", type=bool, default=False, help="if true, then, it deploys the model to sagemaker"
    )
    parser.add_argument(
        "--model_name", "-mn", type=str, default="latest-model-sagemaker", help="model name for deployment on sagemaker"
    )

    # simple config for deployment on Sagemaker
    parser.add_argument(
        "--create_config",
        "-cc",
        type=bool,
        default=False,
        help="create a simple config dict to push the image to sagemaker",
    )
    parser.add_argument("--config", "-c", type=json.loads, default=None, help="config for pushing image to sagemaker")
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
    parser.add_argument("--image_uri_ecr", "-iu", type=str, default=None, help="image uri on ECR")
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


def download_s3(model_folder_name_s3: str, folder: str) -> str:
    """Downloading files from s3 bucket folder

    :param model_folder_name_s3:
    :param folder:
    :return:

    e.g.
    model_folder_name_s3 = s3://s3-bucket-name/1234/5678/artifacts/GradientBoost
    folder = download
    """

    def separate_path(model_folder_name_smh: str) -> Tuple[str, str]:
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

    return cur_path


if __name__ == "__main__":
    args = parse_args()

    # registration image to ECR
    with open("registry.sh", "w") as f:  # create a folder at this dir
        model_uri_local_folder = download_s3(args.model_folder_name_s3, args.folder)
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
    subprocess.call("registry.sh", shell=True)

    # deployment to Sagemaker
    if args.deployment:
        if args.create_config:
            config = create_simple_dict_for_sagemaker(
                execution_role_arn=args.execution_role_arn,
                bucket=args.bucket_name_for_sagemaker,
                image_uri_ecr=args.image_uri_ecr,
                region_name=args.region_name,
                instance_type=args.instance_type,
                instance_count=args.instance_count,
            )
        else:
            config = args.config

        deploy_model_to_sagemaker(args.model_name, model_uri_local_folder, config)
