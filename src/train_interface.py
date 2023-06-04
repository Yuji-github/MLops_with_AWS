import numpy as np
from abc import ABC, abstractmethod
from typing import Any
import mlflow


class TrainInterface(ABC):
    """All machine learning model carry this interface"""

    def __init__(self, mlflow: mlflow) -> None:
        """
        :param mlflow:
        """
        self.model_name: str
        self.model: Any
        self.random_state: int = 42
        self.n_estimators_range = np.arange(100, 500, 25)
        self.max_depth_range = np.arange(1, 25, 2)
        self.learning_rate_range = [0.1, 0.05, 0.01, 0.005, 0.001]
        self.mlflow: mlflow = mlflow

    def initialise_model(self, model: list) -> None:
        """Initializing model

        :param model:
        :return None:
        """
        self.model = model[0]
        self.model_name = model[1]

    @abstractmethod
    def _train(self, x_train: np.array, y_train: np.array, x_test: np.array, **kwargs) -> np.array:
        """All machine learning models need to create this function

        :param x_train:
        :param y_train:
        :param x_test:
        :param kwargs:
        :return np.array:
        """
        raise NotImplementedError

    @abstractmethod
    def _evaluate(self, y_test: np.array, y_pred: np.array) -> Any:
        """All machine learning models need to create this function

        :param y_test:
        :param y_pred:
        :return Any:
        """
        raise NotImplementedError
