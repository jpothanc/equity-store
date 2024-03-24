import os

def get_env_config_file():
    env = os.getenv('FLASK_ENV', '')
    # We should not default environments as it can lead to unexpected behavior
    # but for ease of use we are defaulting to development
    if env == '':
        env = 'development'
        # raise Exception("FLASK_ENV is not set")
    file_path = os.path.join("appsettings","config", f"config.{env}.json")
    return file_path

def get_env_factory_file():
    env = os.getenv('FLASK_ENV', '')
    # We should not default environments as it can lead to unexpected behavior
    # but for ease of use we are defaulting to development
    if env == '':
        env = 'development'
        # raise Exception("FLASK_ENV is not set")
    file_path = os.path.join("appsettings","factory", f"factory.{env}.json")
    return file_path