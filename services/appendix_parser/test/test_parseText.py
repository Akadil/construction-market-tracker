import logging
from Parsetext import Parsetext

logging.basicConfig(level=logging.DEBUG, 
            format='[%(name)s] - %(levelname)s - %(message)s')


def main():
    logging.info("Starting the program")
    
    # open the file and read the content
    for i in range(1, 10):

        with open(f"test/results/appendix_{str(i)}.txt", "r") as file:
            text = file.read()
        
        try:
            # create an instance of the class
            parser = Parsetext()
        
            # test the function
            result = parser.parse(f"appendix_{str(i)}.txt", text)
            if (result['success'] == False):
                logging.error(f"Error: {result['message']}")
                break
            
            logging.info(f"Success: appendix_{str(i)}.txt")
            logging.info(f"Data: {result['data']}")
            
        except Exception as e:
            logging.error(f"{str(e)}")
    

if __name__ == "__main__":
    main()