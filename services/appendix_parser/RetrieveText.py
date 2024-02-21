from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from io import StringIO
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s: %(message)s')

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
                - Implement a proper logging
                - Write the tests

            - Current version / compatibility / dependencies
                - 

        @version    1.0
    """

    def __init__(self):
        self.output_string = StringIO()
        self.interpreter = None


    def get_text(self, file_path):
        """
            Main function of a class. It reads a file and returns its content.
        """
        text = None
        try:
            with open(file_path, 'rb') as file:
                logging.info(f"Reading the file: {file_path}")

                # get pages using pdfminer
                pages = self.get_all_pages(file)
                logging.info(f"Number of pages: {len(pages)}")

                # filter out the unneeded pages (Kaz and description pages)
                pages = self.filter_pages(pages)

                # extract text from the pages using pdfminer
                for page in pages:
                    self.interpreter.process_page(page)

                text = self.output_string.getvalue()
                if (text == None or text == ""):
                    raise CustomException("Couldn't get the text ")
                
                # Remove bad content using the key words
                text = self.filter_text(text)

        except Exception as e:
            logging.error(f"{str(e)}")  # @todo - log the proper error
            return None

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
            raise CustomException("Couldn't get the pages from the file")
        elif (len(pages) <= 2):
            raise CustomException("The number of pages is not enough")

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
            raise CustomException("The text is not in the proper format")

        text = text[position + len(qwe):]

        # remove the second part of the beginning of the table
        qwe = "предложение"
        position = text.find(qwe)
        if (position == -1):
            raise CustomException("The text is not in the proper format")

        text = text[position + len(qwe):]

        # remove the end of the table
        qwe = "Примечание"
        position = text.find(qwe)
        if (position == -1):
            raise CustomException("The text is not in the proper format")

        text = text[:position]

        logging.debug(f"Filtered text: {text}")
        return text
