# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    dept = scrapy.Field()

class DegreeItem(scrapy.Item):
    name = scrapy.Field()
    degType = scrapy.Field()
    date_updated = scrapy.Field()
    dept = scrapy.Field()
    courses = scrapy.Field()
    groups = scrapy.Field()
    total_units = scrapy.Field()
