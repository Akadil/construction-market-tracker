import yaml

def main():
    """
        Test:   Practice using the config.yaml files how the data can be stored 
                and used

        Questions:  
            1.  What is the nature of retrieved data?
            2.  What data structure I can ues inside of the config file?
    
        Results:    it is just a dictionary of data
    
            Questions:
                1. Just a dictionary: {'MSG': 'Hello, World!'}
                2. 
                    - No set
                    - I can use a list, dict, text, number, boolean, float
    """

    print("Hello, world!")

    # open the config file
    with open('zone_practice/test_config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        print(data)


if __name__ == "__main__":
    main()