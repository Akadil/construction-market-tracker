def main():
    """=================================================================="""
    """
        Test: Test if key is in dict

        Result: It works                  
    """
    """=================================================================="""
    myDict = dict()

    myDict["key1"] = "value1"
    myDict["key2"] = "value2"

    if ("key1" in myDict):
        print("key1 is in myDict")
    else:
        print("key1 is not in myDict")

if __name__ == "__main__":
    main()