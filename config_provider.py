import yaml
import logging

class ConfigProvider:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.load_config()
        self.validate_config(self.config_data)

    def load_config(self):
        """
        Load and parse the YAML config file.
        """
        try:
            with open(self.config_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML file : {e}")

    def validate_config(self, config_data):
        """
        Dynamically validate the structure of the YAML configuration file.
        """
        def validate_node(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    if isinstance(value, (dict, list)):
                        validate_node(value)
                    elif not isinstance(value, (str, int, float, bool, type(None))):
                        raise ValueError(f"Invalid value type for key {key}: {type(value)}")
            elif isinstance(node, list):
                for item in node:
                    if isinstance(item, (dict, list)):
                        validate_node(item)
                    elif not isinstance(item, (str, int, float, bool, type(None))):
                        raise ValueError(f"Invalid value type for key {item}: {type(item)}")
            else:
                if not isinstance(node, (str, int, float, bool, type(None))):
                    raise ValueError(f"Invalid value type for key {node}: {type(node)}")

        if not isinstance(config_data, dict):
            raise ValueError("Root of the config file must be a dictionary.")
        validate_node(config_data)
        logging.info("Config file validated successfully.")