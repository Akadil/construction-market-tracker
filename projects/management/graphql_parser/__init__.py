import os
import yaml

def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    else:
        raise FileNotFoundError("Configuration file not found")

# Example usage
config_file = 'config.yml'
try:
    config = load_config(config_file)
    print("Configuration loaded successfully:", config)
except FileNotFoundError as e:
    print("Configuration file not found")
    raise ImportError(f"[GraphQL parser] Error: {str(e)}")
