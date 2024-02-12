
def get_file_link(files: list, nameFile: str) -> str:
    """
        This function takes a list of files and a name of the file in Russian
        and returns the link to the file.

        Returns:
            str: The link to the file

        Possible inputs:
            files: list: A list of files
            nameFile: str: The name of the file. E.g. "buy_pi", "appendix_5"
    """

    for file in files:
        if nameFile in file["originalName"]:
            return (file["originalName"], file["filePath"])
    return None