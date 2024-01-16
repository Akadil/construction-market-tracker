import scrapy
import logging
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from dirtyPast.items import PastTender

def clean_text(value):
    return value.replace('\r\n', '').strip() if value else None

def compare_strings(string1, string2):
    differences = [string1, string2]

    # Check length
    if len(string1) != len(string2):
        differences.append(f"Lengths are different. {len(string1)} vs {len(string2)})")

    # Compare character by character
    for i, (char1, char2) in enumerate(zip(string1, string2)):
        if char1 != char2:
            differences.append(f"Difference at position {i}: '{char1}' vs '{char2}'")

    # Check for hidden characters or encoding issues
    for i, (char1, char2) in enumerate(zip(string1.encode(), string2.encode())):
        if char1 != char2:
            differences.append(f"Encoding difference at position {i}: '{hex(char1)}' vs '{hex(char2)}'")

    return differences

class PasttendersSpider(scrapy.Spider):
    name = "pastTenders"
    allowed_domains = ["goszakup.gov.kz"]
    start_urls = ["https://goszakup.gov.kz/ru/eDepository/dataWorkPerformed/subject/91848?&page=1"]

    def parse(self, response):
        logger = logging.getLogger(__name__)

        # Extract data from each row in the table
        rows = response.css('table.table.table-bordered tr.complaint-green')

        for row in rows:
            # past_tender = PastTender(
            #     number=row.css('td:nth-child(1) a::text').get(),
            #     name=row.css('td:nth-child(2)::text').get(),
            #     status_supplier=row.css('td:nth-child(3)::text').get(),
            #     completion_year=row.css('td:nth-child(4)::text').get(),
            #     construction_type=row.css('td:nth-child(5)::text').get(),
            #     address=row.css('td:nth-child(6)::text').get(),
            #     customer_name=row.css('td:nth-child(7)::text').get(),
            #     status_info=row.css('td:nth-child(8)::text').get(),
            #     responsibility_level=row.css('td:nth-child(9)::text').get(),
            #     technical_complexity=row.css('td:nth-child(10)::text').get(),
            #     functional_purpose=row.css('td:nth-child(11)::text').get(),
            # )

            loader = ItemLoader(item=PastTender(), selector=row)

            # Define selectors for each field and apply processors
            loader.add_css('number', 'td:nth-child(1) a::text')
            loader.add_css('name', 'td:nth-child(2)::text')
            loader.add_css('status_supplier', 'td:nth-child(3)::text', MapCompose(clean_text))
            loader.add_css('completion_year', 'td:nth-child(4)::text')
            loader.add_css('construction_type', 'td:nth-child(5)::text')
            loader.add_css('address', 'td:nth-child(6)::text')
            loader.add_css('customer_name', 'td:nth-child(7)::text')
            loader.add_css('status_info', 'td:nth-child(8)::text')
            # loader.add_css('responsibility_level', 'td:nth-child(9)::text', Compose(lambda v: v.replace('\r\n', '').strip() if v else None))
            # loader.add_css('technical_complexity', 'td:nth-child(10)::text', Compose(lambda v: v.replace('\r\n', '').strip() if v else None))
            # loader.add_css('functional_purpose', 'td:nth-child(11)::text', Compose(lambda v: v.replace('\r\n', '').strip() if v else None))
            loader.add_css('responsibility_level', 'td:nth-child(9)::text', MapCompose(clean_text))
            loader.add_css('technical_complexity', 'td:nth-child(10)::text', MapCompose(clean_text))
            loader.add_css('functional_purpose', 'td:nth-child(11)::text', MapCompose(clean_text))

            # logger.info("\n\n~~~~~~~~~Processing item: %s\n\n\n", loader.get_output_value('status_info'))

            # Conditionally check and filter data
            # if loader.get_output_value('number') is None:
            #     return
            # if int(loader.get_output_value('completion_year')[0]) <= 2013:
            #     return
            status_info = loader.get_output_value('status_info')

            if status_info is None or len(status_info) == 0:
                continue
            status_info = status_info[0]
            if status_info != 'Подтверждено':
                reasons = compare_strings(status_info, 'Подтверждено')
                logger.info("\n\n")
                print(loader.get_output_value('status_info'))
                for reason in reasons:
                    logger.info("%s\n", reason)
                logger.info("\n\n")
                continue
            # if loader.get_output_value('functional_purpose') != 'объекты жилищно-гражданского назначения':
            #     return

            # Load the item
            past_tender = loader.load_item()
            yield past_tender

        next_page_link = response.css('ul.pagination li:contains(">") a::attr(href)').get()

        if next_page_link:
            yield scrapy.Request(url=next_page_link, callback=self.parse)
