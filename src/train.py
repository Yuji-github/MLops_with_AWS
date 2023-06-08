import numpy as np
from mlflow.models import ModelSignature
from train_interface import TrainInterface
from sklearn.metrics import accuracy_score
from typing import Any


class Train(TrainInterface):
    """Training machine learning"""

    def _train(self, x_train: np.array, y_train: np.array, x_test: np.array, **kwargs) -> np.array:
        """Training model with given params from main, then, return prediction

        :param x_train:
        :param y_train:
        :param x_test:
        :param kwargs:
        :return np.array:
        """

        self.model.learning_rate = kwargs["learning_rate"]
        self.model.n_estimators = kwargs["n_estimators"]
        self.model.max_depth = kwargs["max_depth"]

        self.model.fit(x_train, y_train)
        return self.model.predict(x_test)

    def _evaluate(self, y_test: np.array, y_pred: np.array) -> Any:
        """Evaluating model performance with prediction and grand-truth

        :param y_test:
        :param y_pred:
        :return accuracy:
        """
        return accuracy_score(y_test, y_pred)

    def _logging_params_to_mlflow(self, learning_rate: float, n_estimators: int, max_depth: int) -> None:
        """Logging params to MLflow

        :param learning_rate:
        :param n_estimators:
        :param max_depth:
        :return None:
        """

        self.mlflow.log_param("learning_rate", learning_rate)
        self.mlflow.log_param("n_estimators", n_estimators)
        self.mlflow.log_param("max_depth", max_depth)

    def _logging_eval_to_mlflow(self, accuracy: float) -> None:
        """Logging performance to MLflow

        :param accuracy:
        :return None:
        """

        self.mlflow.log_metric("accuracy", accuracy)

    def _logging_model_to_mlflow(self, signature: ModelSignature) -> None:
        """Logging the model and model name to MLflow

        :return None:
        """
        if self.model_name == "lightGBM":
            self.mlflow.lightgbm.log_model(self.model, artifact_path=self.model_name, signature=signature)
        elif self.model_name == "GradientBoost":
            self.mlflow.sklearn.log_model(self.model, artifact_path=self.model_name, signature=signature)
