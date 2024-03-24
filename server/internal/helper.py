import os

def get_env_config_file():
    env = os.getenv('FLASK_ENV', 'development')
    file_path = os.path.join("appsettings","config", f"config.{env}.json")
    return file_path

def get_env_factory_file():
    env = os.getenv('FLASK_ENV', 'development')
    file_path = os.path.join("appsettings","factory", f"factory.{env}.json")
    return file_path