import camelot

def main():
    """ ====================================================================="""
    """
        Test: Test the usage of camelot to parse a pdf file
        
        Results: It appeared to be really hard to install its dependencies.
                I couldn't install opencv Library which is required for 
                camelot python code. I have no idea why do I need computer 
                vision for my task
    """
    """ ====================================================================="""
    pdf_path = 'examples/appendix.pdf'
    tables = camelot.read_pdf(pdf_path, flavor='stream', pages='all')

    for i, table in enumerate(tables):    
        print(f"Table {i + 1}:\n{table.df}\n")

if __name__ == "__main__":
    main()
