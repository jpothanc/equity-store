from abc import abstractmethod

class DatabaseService:
    @abstractmethod
    def query(self, connection_string, query):
        pass

