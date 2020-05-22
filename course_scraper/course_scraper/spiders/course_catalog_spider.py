
from __future__ import print_function
import json
import re
import logging

import scrapy
from scrapy.http.request import Request
from course_scraper.items import CourseItem
from scrapy.http import Request, FormRequest
from scrapy.exceptions import CloseSpider

# from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class Course_Catalog_Spider(scrapy.Spider):
    name = "course_catalog"
    handle_httpstatus_list = [999]

    def __init__ (self, domain=None):
        #self.accountName = accountName
        self.start_urls = ["https://www.scc.losrios.edu/2020-2021-catalog/programs-of-study/list-of-programs/accounting"]
        self.currentIndex = 0
        self.dept_urls = []
        self.depts = ["Accounting"]

    def parse(self, response):
        # departments = response.xpath('//div[@class="side-nav"]').css('a::href')
        courses = response.css('div#tab-3')
        # response.css("ul.directory.dir-col > li > a::attr('href')")
        # If first pass, grab and store departments and their URL's
        if self.currentIndex == 0:
            departments = response.xpath('//div[@class="side-nav"]').xpath('//li[@class="parent opened child"]').css('ul')
            listings = departments.css('li')[8].css('ul')
            for d in listings:
                self.depts.append(d.css('a::text').extract())
                self.dept_urls.append(d.css('a::attr(href)').extract())

            print(self.dept_urls)
            print(self.depts)

        course_names = courses.css('h3::text')

        if (courses and (response.status == 200)):
            for course in course_names:
                item = CourseItem()
                item['title'] = course.extract()
                item['dept'] = response.css('h1::text').get()
                yield item

        self.currentIndex += 1
        print(self.currentIndex)

        next_dept_url = self.dept_urls[0][self.currentIndex]
        next_url = response.urljoin(next_dept_url)

        print(next_url)

        if next_url:
            yield scrapy.Request(next_url, self.parse)

    # def fill_details(self, response, item)
    #     details = response.css('ul')
    #     for d in details:
    #         item['units'] = d.css('li::text')[0].get()

    #             #prereq: d.css('li::text')[2].get()
    #             # item['hours'] = course.css('ul.details-list _flex-list.label::text')[1].get()
    #             # item['prereq'] = course.css('ul.details-list _flex-list.label::text')[2].get()
    #             # item['advisory'] = course.css('ul.details-list _flex-list.label::text')[3].get()
    #             # item['posted_date'] = course.css('ul.details-list _flex-list.label::text')[4].get()
    #             # item['description'] = course.css('ul.details-list _flex-list.label::text')[4].get()
    #         yield item

    #         next_link = response.url
    #         self.currentIndex += 1
    #         next_link = next_link[:next_link.find(self.accountName)] + self.accountName + '&start=' + str(25 * self.currentIndex)
    #        yield scrapy.Request(next_link, callback=self.parse)
