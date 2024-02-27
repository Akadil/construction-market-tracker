def main():
    """
        Test the nature of the passed parameter
    """

    # Example usag
    text = "Hello world"

    print(f"Original text with a string: {text}")
    modify_text(text)
    print(f"Modified text wth a string: {text}")


    modify_text_list([text])
    print(f"Modified text wth a list: {text}")


    text_list = [text]
    modify_text_list(text_list)
    print(f"Modified text wth creating a list: {text_list[0]}")


def modify_text(text):
    """
        This function modifies the text

        :param text: string

        :return: modified text
    """

    text = text + " modified"


def modify_text_list(text):
    """
        This function modifies the text

        :param text: string

        :return: modified text
    """

    text[0] = text[0] + " modified"


if __name__ == "__main__":
    main()