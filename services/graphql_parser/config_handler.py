import yaml

class ConfigHandler:
    data: dict

    def __init__(self, config_file: str = None):
        # Load the configuration file
        try:
            if config_file:
                with open(config_file, 'r') as f:
                    self.data = yaml.safe_load(f)
            else:
                with open('projects/management/graphql_parser/config.yml') as f:
                    self.data = yaml.load(f, Loader=yaml.FullLoader)

        except FileNotFoundError as e:
            print("[Config handler] Error: Configuration file not found")
            raise ImportError(str(e))

    def get(self, value: str):
        return self.data[value]

    def get_allKato(self):
        returner = []

        for kato in self.data['kato']:
            returner.append(kato)
        return returner


    def get_tradeMethod_id(self):
        """
            Returns the trade method id that is used to filter the tenders
        """
        returner = []

        for trade_method in self.data['REF_TRADE_METHODS_VALUES']:
            if trade_method['id'] == 188:
                returner.append(trade_method['id'])
        return returner


    def get_statusFinished_id(self):
        """
            Returns the status id that is used to filter the tenders
        """
        returner = []

        for status in self.data['REF_LOTS_STATUS_VALUES']:
            if status['id'] == 350:
                returner.append(status['id'])
        return returner

# if __name__ == '__main__':
#     config = ConfigHandler()
#     while True:
#         str = input('Enter the key: ')
#         print(config.get(str))