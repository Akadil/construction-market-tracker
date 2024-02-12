import yaml

def main():
    with open('projects/management/graphql_parser/config.yml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        query = data['REGISTRY_SUBJECT_TYPE']
    print(query)

if __name__ == '__main__':
    main()