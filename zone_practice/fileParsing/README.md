## Parse the documents to retrieve project specifications

#### Ways to parse the pdf
- <b>PyPDF2</b>
    - [Medium Link](https://medium.com/@inzaniak/pypdf-a-brief-introduction-to-pdf-manipulation-in-python-ca2dc5ce7122) of short introduction to package. IT IS FUCKING LOCKED!
    - [Documentation Link](https://pypdf.readthedocs.io) Official documentation
    - I can extract the full text of the page and then use regex to get specific information
- <b>tabula-py</b>
    - tabula-py is a simple Python wrapper of tabula-java, which can read table of PDF. You can read tables from PDF and convert them into pandas’ DataFrame. tabula-py also converts a PDF file into CSV/TSV/JSON file.
    - [Documentation Link](https://tabula-py.readthedocs.io/en/latest/getting_started.html) 
- <b>camelot</b>
    - Seems like latest solution whose results are better in performance than other solutions
    - [Documentation Link](https://camelot-py.readthedocs.io/en/master/)

- <b>PdfMiner</b> 
    - Simple text parser. Get the text, then use proper regex


#### Ways to parse the html file
- <b>BeautifulSoup</b>  
    - [Link](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for documentation