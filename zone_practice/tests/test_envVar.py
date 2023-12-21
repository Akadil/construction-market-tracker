from dotenv import dotenv_values
import os

"""
    @brief Test the env variables retrieval

    @results -  Evrythings works fine, just need to check for existence of file and key

    @attention -  Not existing values causes error (KeyError)
                    |-> @solution use try catch for that or check for existence
    @attention -  Not existing .env file causes error (keyyError)
                    |-> @solution similar solution as above
                                    maybe check for existence of file
"""
def main():

    env_vars = dotenv_values('.env')

    print("====================================")
    print("Testing env variables retrieval:")
    print("====================================\n")

    # Show full information about env variables
    if (env_vars.__len__() == 0):
        print("Error: No env variables or no file .env\n")
        return
    else:
        print("Env variables (full):\n")
        print(env_vars, "\n\n")

    # Show proper one
    if (env_vars.keys().__contains__("TOKEN")):
        print("Env variables (TOKEN):\n")
        print(f'Token: {env_vars["TOKEN"]}', "\n\n")
    else:
        print("Error: No TOKEN env variable\n")

    # Show wrong one
    # print("\nEnv variables (WRONG_TOKEN):\n")
    # print(f'Token: {env_vars["WRONG_TOKEN"]}\n')

if __name__ == "__main__":
    main()