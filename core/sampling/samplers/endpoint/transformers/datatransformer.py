from abc import abstractmethod, ABC


class DataTransformer(ABC):

    @abstractmethod
    def transform(self, res):
        pass
