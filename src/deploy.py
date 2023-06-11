from mlflow.deployments import get_deploy_client


def create_simple_dict_for_sagemaker(
    execution_role_arn: str, bucket: str, image_uri_ecr: str, region_name: str, instance_type: str, instance_count: int
) -> dict:
    """Creating a simple dict for deploy_model_to_sagemaker function
    If you want to have a custom dict for pushing the model to sagemaker, pass the custom dict directly to the function

    :param execution_role_arn:
    :param bucket:
    :param image_uri_ecr:
    :param region_name:
    :param instance_type:
    :param instance_count:
    :return dict:
    """

    return dict(
        execution_role_arn=execution_role_arn,
        bucket=bucket,
        image_uri=image_uri_ecr,
        region_name=region_name,
        instance_type=instance_type,  # https://aws.amazon.com/sagemaker/pricing/
        instance_count=instance_count,
    )


def deploy_model_to_sagemaker(model_name: str, model_uri_local_folder: str, config: dict) -> None:
    """Deploying a model to sagemaker (end point).
    The execution time will be longer if the model is large

    Sample config:
     config = dict(
        execution_role_arn="arn:aws:iam::123456789:role/service-role/AmazonSageMaker-ExecutionRole-123456789",
        bucket="sagemaker-mlflow-with-aws",
        image_uri="1234567899.dkr.ecr.ap-southeast-2.amazonaws.com/for-sagemaker-deployment",
        region_name="ap-southeast-2",
        instance_type="ml.c5.large",
        instance_count=1,
    )

    :param model_name:
    :param model_uri_local_folder:
    :param config:
    :return None:
    """

    client = get_deploy_client("sagemaker")
    client.create_deployment(
        name=model_name,
        model_uri=model_uri_local_folder,
        config=config,
    )
