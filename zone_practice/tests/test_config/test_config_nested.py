import yaml
import os

def main():

    with open("zone_practice/tests/test_config/config.yml", "r") as file:
        config = yaml.safe_load(file)
        variable = config["variable"]

    # Retrieve the variable instances
    print(variable)


if __name__ == "__main__":
    main()