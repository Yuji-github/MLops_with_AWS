from unittest import TestCase
import unittest
from deploy import create_simple_dict_for_sagemaker


class TestDeploy(TestCase):
    def test_create_simple_dict_for_sagemaker(self):
        """Testing create_simple_dict_for_sagemaker

        :except same dict values:
        """

        expect_dict = dict(
            execution_role_arn="arn:aws:iam::123456789:role/service-role/AmazonSageMaker-ExecutionRole-123456789",
            bucket="sagemaker-mlflow-with-aws",
            image_url="1234567899.dkr.ecr.ap-southeast-2.amazonaws.com/for-sagemaker-deployment",
            region_name="ap-southeast-2",
            instance_type="ml.c5.large",
            instance_count=1,
        )

        test_result = create_simple_dict_for_sagemaker(
            execution_role_arn="arn:aws:iam::123456789:role/service-role/AmazonSageMaker-ExecutionRole-123456789",
            bucket="sagemaker-mlflow-with-aws",
            image_url_ecr="1234567899.dkr.ecr.ap-southeast-2.amazonaws.com/for-sagemaker-deployment",
            region_name="ap-southeast-2",
            instance_type="ml.c5.large",
            instance_count=1,
        )

        self.assertEqual(expect_dict, test_result)


if __name__ == "__main__":
    unittest.main()
