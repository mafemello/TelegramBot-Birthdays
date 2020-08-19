from abc import ABC,abstractmethod

# class that represents the APIs
class AbstractAPI(ABC):
    def __init__(self, arguments):
        self._arguments = arguments

    
    @abstractmethod
    def get_message(self):
        print("Abstract Method")