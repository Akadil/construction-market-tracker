import os
import sys
import re
import json

from pdfminer.high_level import extract_text
import logging
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


dir_path = "services/appendix_parser/"
output_string = StringIO()
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
    """
        This functions uses pdfminer to extract text 
    """
    try:
        # text = extract_text(pdf_path)
        
        text = None
        with open(pdf_path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # extract text from the last 2 pages
            pages = []
            for page in PDFPage.create_pages(doc):
                pages.append(page)
                # interpreter.process_page(page)

            if (len(pages) <= 2):
                raise CustomException("Error: The number of pages is less than 2")
            
            for page in pages[int(len(pages) / 2):]:
                interpreter.process_page(page)

            text = output_string.getvalue()

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
        # name = dir_path + f"practice/files_in_text/text{file[-5]}.txt"
        # with open(name, "w") as f:
        #     f.write(text)


        input("Press Enter to continue...")

# print the list of files and their text
if __name__ == "__main__":
    main()
