import os
import sys
import re
import json

from pdfminer.high_level import extract_text
import logging

dir_path = "services/appendix_parser/"

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')


def get_files_list():
    # get the list of all files from examples folder
    examples_folder = os.path.join(os.getcwd(), dir_path + 'examples')
    files_list = os.listdir(examples_folder)

    # filter out unnecessary files
    filtered_files_list = []

    for file in files_list:
        if "appendix" in file:
            filtered_files_list.append(file)
    
    logging.info(f"Filtered files list: {filtered_files_list}")
    return filtered_files_list


def get_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        
        if text is None:
            raise CustomException("Error: The text could not be extracted")
    
    except Exception as e:
        logging.error(f"{str(e)}")
        return None

    return text


def main():
    filtered_files_list = get_files_list()
    for file in filtered_files_list:
        file_path = os.path.join(os.getcwd(), dir_path + 'examples', file)
        text = get_text_from_pdf(file_path)
        
        # logging.INFO(f"File: {file}, Text: {text}")
        print(f"File: {file}, Text: {text}")

        # write the text into a file
        name = dir_path + f"practice/files_in_text/text{file[-5]}.txt"
        with open(name, "w") as f:
            f.write(text)

        input("Press Enter to continue...")

# print the list of files and their text
if __name__ == "__main__":
    main()
