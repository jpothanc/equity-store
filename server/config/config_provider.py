import json


class ConfigProvider:
    def __init__(self, config_file):
        self.config_file = config_file
        self.data = self.load()

    def load(self):
        with open(self.config_file, 'r') as file:
            data = json.load(file)
        return data

    def get(self, key):
        return self.data[key] if key in self.data else None
