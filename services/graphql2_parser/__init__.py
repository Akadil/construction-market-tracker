from dotenv import dotenv_values
from config_handler import ConfigHandler
# import yaml

# Example usage
try:
    # with open('config.yml', 'r') as f:
    #     config = yaml.safe_load(f)

    config = ConfigHandler()

    env_variables = dotenv_values('.env')
    token = env_variables['TOKEN']

except Exception as e:
    print(f"[GraphQL parser] Error: {str(e)}")
    raise ImportError(str(e))
