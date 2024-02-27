import logging
import sys
sys.path.append('/mnt/nfs/homes/akalimol/my_git/gss_market')

from services.appendix_parser.Parsetext import Parsetext

logging.basicConfig(level=logging.DEBUG, 
            format='[%(name)s] - %(levelname)s - %(message)s')

myPath = "services/appendix_parser/"

def main():
    logging.info("Starting the program")
    
    # open the file and read the content
    for i in range(1, 10):
        with open(f"{myPath}/examples/rt_results/appendix_{str(i)}.txt", "r") as file:
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