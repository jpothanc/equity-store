import json

from injector import Injector, inject

from services.encryption_service import EncryptionService


class ConfigProvider:
    @inject
    def __init__(self,injector : Injector, config_file = "config.json"):
        self.config_file = config_file
        self.encrypt_service = injector.get(EncryptionService)
        self.data = self.load()

    def load(self):
        with open(self.config_file, 'r') as file:
            data = json.load(file)
        return data

    def get(self, key):
        return self.data[key] if key in self.data else None

    def get_connection_string(self, data_source_name):
        data_source =  self.data["data_sources"][data_source_name] if data_source_name in self.data["data_sources"] else None
        password = self.encrypt_service.decrypt(data_source['password'])
        connection_string = data_source['connection_string'].format(username=data_source['username'], password=password, host=data_source['host'], database=data_source['database'])
        return connection_string