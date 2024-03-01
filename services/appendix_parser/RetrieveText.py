import logging

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import yaml
import re

from io import StringIO

# logging.getLogger().setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

class RetrieveText:
    """
        The class designed to receive a file path and return the specific text 
        from the file. The class uses pdfminer to extract the text

        Methods:
            get_text(file_path) -> str: 
                Main function of a class. It reads a file and returns its 
                content. The subsequent functions are called from this function
            
            get_all_pages(file) -> list(): Extract all pages from the file. This
                function uses pdfminer to extract pages
            
            filter_pages(pages) -> list(): This function filters out the 
                unneeded pages. It receives a proper list of pages and returns 
                a filtered list of pages. It focuses only on the proper content
            
            filter_text(text) -> str: This function removes everything except 
                the table content

        Additionally:
            - Future @todo tasks
                - lots of work. Very dirty code and a lot of exceptions

            - Current version / compatibility / dependencies
                - 

        @version
            - 2.0 Finished
            - The test file is test/test_retrieveText.py
            - 27.02 version
            - The logs are normal
    """
    config: dict = None     # config file


    def __init__(self, config = None):
        logger.info("Initiating the class")

        self.output_string = StringIO()
        self.interpreter = None

        # import the config file
        try:
            if (config != None):
                self.config = config['RETRIEVETEXT']
            else:
                with open('./config.yml', 'r') as file:
                    data = yaml.safe_load(file)
                    self.config = data['RETRIEVETEXT']
        
        except Exception as e:
            logger.error(f"Failed to init: {e}")


    def retrieve(self, file_path):
        """
            Main function of a class. It reads a file and returns its content.
        """
        logger.info(f"Reading the file: {file_path}")
        
        # Just a precaution
        if self.config == None:
            logger.warning("The config file is not loaded")
            return None

         # Parse the pages
        try:
            logger.info(f"Parsing the pages")

            with open(file_path, 'rb') as file:
                # get pages using pdfminer
                all_pages = self.get_all_pages(file)

                # filter out the unneeded pages (Kaz and description pages)
                pages = self.filter_pages(all_pages)
    
                for page in pages:
                    self.interpreter.process_page(page)
        except Exception as e:
            logger.error(f"{str(e)}")  # @todo - log the proper error
            return None

        # extract text from the pages
        try:
            logger.info(f"Extracting the text from the pages")


            text = self.output_string.getvalue()
            if (text == None or text == ""):
                raise Exception("Couldn't get the text ")
            
            # Remove bad content using the key words
            text = self.filter_text(text)

        except Exception as e:
            logger.error(f"{str(e)}")
            return None

        logger.info(f"Text extracted successfully")
        logger.debug(f"Text: {text}")
        return text


    def get_all_pages(self, file) -> list():
        """
            This function uses pdfminer to extract pages

            :param file: proper and existing file

            :return: Tested and correct pages
        """
        
        # Configure the inner configurations of pdfminer
        self.output_string.seek(0)
        self.output_string.truncate()

        parser = PDFParser(file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, self.output_string, laparams=LAParams())
        self.interpreter = PDFPageInterpreter(rsrcmgr, device)

        # save the pages as a list
        pages = []
        for page in PDFPage.create_pages(doc):
            pages.append(page)
        
        # Check for correctness of the pages
        if (len(pages) == 0):
            raise Exception("Couldn't get the pages from the file")
        elif (len(pages) <= 2):
            raise Exception("The number of pages is not enough")

        
        return pages


    def filter_pages(self, pages):
        """
            This function filters out the unneeded pages. It receives a proper
            list of pages and returns a filtered list of pages. It focuses only
            on the proper content

            :param pages: list of pages

            :return: filtered pages
        """

        len_rus_page = len(pages) / 2
        if (len_rus_page <= 2):
            return pages[int(len_rus_page):]
        else:
            return pages[int(len_rus_page) + 1:]


    def filter_text(self, text):
        """
            This function removes everything except the table content

            :param text: string

            :return: filtered text
        """

        # remove the beginning of the table
        qwe = "6. Сведения о наличии опыты работы для расчета критериев, влияющих на конкурсное ценовое"
        position = text.find(qwe)
        if (position == -1):
            raise Exception("Text wrong format. No beginning of the table")

        text = text[position + len(qwe):]

        # remove the second part of the beginning of the table
        qwe = "предложение."
        position = text.find(qwe)
        if (position == -1):
            raise Exception("Text wrong format. No beginning of the table(2)")

        text = text[position + len(qwe):]

        # remove the end of the table
        qwe = "Примечание"
        position = text.find(qwe)
        if (position == -1):
            raise Exception("Text wrong format. No end of the table")

        text = text[:position]

        return text
