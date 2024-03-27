import yaml

def main():
    """
        The goal is to retrieve the boolean values from the config 
        file and check if they are True or False

        :results
            both of them works
            
    """

    # open the config file using yaml
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
        test = config.get("PRACTICE_TESTS")
        test = test.get("TEST_BOOL")

    # start the test
    print("Checking the big True: \n")
    
    print(f"The value is {test.get('BIG_TRUE')}")
    if (test.get("BIG_TRUE")):
        print("True")
    else:
        print("False")

    print("\nChecking the small True: \n")
    print(f"The value is {test.get('SMALL_TRUE')}")
    if (test.get("SMALL_TRUE")):
        print("True")
    else:
        print("False")

    print("\nChecking the big False: \n")
    print(f"The value is {test.get('BIG_FALSE')}")
    if (test.get("BIG_FALSE")):
        print("True")
    else:
        print("False")


    print("\nChecking the small False: \n")
    print(f"The value is {test.get('SMALL_FALSE')}")
    if (test.get("SMALL_FALSE")):
        print("True")
    else:
        print("False")

if __name__ == "__main__":
    main()