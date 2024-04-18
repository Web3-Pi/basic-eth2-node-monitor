from abc import ABC, abstractmethod
from typing import Any


class DataReader(ABC):

    @abstractmethod
    def query_data(self, args: str | None = None) -> Any:
        pass

    @abstractmethod
    def get_data_source(self) -> str:
        pass
