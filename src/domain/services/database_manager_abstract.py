from abc import ABC, abstractmethod

class DatabaseManagerAbstract(ABC):
    
    @abstractmethod
    def get_connection_string(self) -> str:
        pass