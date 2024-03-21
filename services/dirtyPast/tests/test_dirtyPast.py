import scrapy
from scrapy.crawler import CrawlerProcess
import sys

class YourSpider(scrapy.Spider):
    name = 'your_spider'
    
    def __init__(self, *args, **kwargs):
        super(YourSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
    
    def parse(self, response):
        # Your parsing logic goes here
        # You can extract data from the response using XPath or CSS selectors
        # For example:
        data = {
            'title': response.css('title::text').get(),
            # Add more fields as needed
        }
        yield data

# Define a function to run the spider and access the data directly
def run_spider_and_access_data(start_url):
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',  # Adjust log level as needed
    })
    
    # Store scraped items in a list
    items = []
    
    def item_collected(item, response, spider):
        items.append(item)
    
    process.crawl(YourSpider, start_url=start_url)
    process.signals.connect(item_collected, signal=scrapy.signals.item_scraped)
    process.start()  # The script will block here until the crawling is finished
    
    return items

# Call the function to run the spider and access the data
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <start_url>")
        sys.exit(1)
    
    start_url = sys.argv[1]
    scraped_data = run_spider_and_access_data(start_url)
    
    # Print the scraped data
    for data in scraped_data:
        print(data)
