import requests
import urllib3
import mimetypes

urllib3.disable_warnings()

def main():
    """ ================================================================== """
    """
        Goal:   Download a file from the internet and save it to the 
                local machine
    """
    """ ================================================================== """

    file_link = "https://ows.goszakup.gov.kz/download/trd_buy/3dea360623afa73945f2666d51ac24fd"

    download_and_save_file(file_link)


def download_and_save_file(url):
    # Download the file
    response = requests.get(url, verify=False)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    
        # Create a file name based on the current timestamp and file extension
        file_name = f'downloaded_file.html'
        
        # Open the file in binary write mode ('wb')
        with open(file_name, 'wb') as file:
            # Write the content to the file
            file.write(response.content)
        
        print(f"File downloaded and saved as '{file_name}'")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

        print("Putain! Something went wrong.")

if __name__ == "__main__":
    main()