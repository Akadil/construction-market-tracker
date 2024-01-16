# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PastTender(scrapy.Item):
    number = scrapy.Field(default=None)
    name = scrapy.Field(default=None)
    status_supplier = scrapy.Field(default=None)
    completion_year = scrapy.Field(default=None)
    construction_type = scrapy.Field(default=None)
    address = scrapy.Field(default=None)
    customer_name = scrapy.Field(default=None)
    status_info = scrapy.Field(default=None)
    responsibility_level = scrapy.Field(default=None)
    technical_complexity = scrapy.Field(default=None)
    functional_purpose = scrapy.Field(default=None)

