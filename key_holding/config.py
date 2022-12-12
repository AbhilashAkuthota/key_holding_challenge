import os
from configparser import ConfigParser

config_path = os.environ.get("CONFIG_PATH", "configs/local.cfg")
base_config_path = "configs/local.cfg"

config = ConfigParser()
config.read([base_config_path, config_path])
