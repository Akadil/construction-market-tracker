import tabula

def main():
    """====================================================================="""
    """
        Test: Test the usage of tabula to parse pdf files
    """
    """====================================================================="""

    pdf_path = 'examples/appendix_5.pdf'
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_pages=True)

    if (len(tables) == 0):
        print("No tables found in the pdf file")
    elif (len(tables) == 1):
        table = tables[-1]

    # print(tables[1].iloc[11, 1])


if __name__ == "__main__":
    main()