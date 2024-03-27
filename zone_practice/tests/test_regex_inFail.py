import regex as re

def main():
    """
        Test the output of the regex.search function when it fails
    """

    text = "My name is ${name} and I am ${age} years old"

    # This regex will succeed
    match = re.search(r"\${[a-zA-Z0-9]+}", text)
    print(match)

    # This regex will fail
    match = re.search(r"\${q[a-zA-Z0-9_]+}", text)
    if (match):
        print("Match found")
    else:
        print("Match not found")


if __name__ == "__main__":
    main()