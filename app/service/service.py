from abc import ABC, abstractmethod

class DataStore(ABC):

    @abstractmethod
    def get_count(self, profile_id: str):
        pass

    @abstractmethod
    def increment_count(self, profile_id: str):
        pass

    @abstractmethod
    def decrement_count(self, profile_id: str):
        pass
