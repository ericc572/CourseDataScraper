
from __future__ import print_function
import json
import re
import logging

import scrapy
from scrapy.http.request import Request
from course_scraper.items import CourseItem
from scrapy.http import Request, FormRequest
from scrapy.exceptions import CloseSpider
from scrapy.http.request import Request
from course_scraper.items import DegreeItem
from scrapy.http import Request, FormRequest
from scrapy.exceptions import CloseSpider

# from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class DegreeSpider(scrapy.Spider):
    name = "degree_spider"
    handle_httpstatus_list = [999]

    def __init__ (self, domain=None):
        self.start_urls = ["https://www.scc.losrios.edu/2020-2021-catalog/programs-of-study/list-of-programs/accounting"]
        self.groupNum = 0
        self.currentIndex = 0
        self.dept_urls = []
        self.depts = ["Accounting"]

    def parse(self, response):
        degree = response.css('div#tab-2')
        # If first pass, grab and store departments and their URL's
        if self.currentIndex == 0:
          departments = response.xpath('//div[@class="side-nav"]').xpath('//li[@class="parent opened child"]').css('ul')
          listings = departments.css('li')[8].css('ul')
          for d in listings:
              self.depts.append(d.css('a::text').extract())
              self.dept_urls.append(d.css('a::attr(href)').extract())

          print(self.dept_urls)
          print(self.depts)

        degree_names = degree.css('h3::text')

        for index, deg in enumerate(degree_names):
          # print("iterating: #")
          # print(index)
          self.groupNum = 0
          degItem = DegreeItem()
          degItem['name'] = deg.extract()
          degItem['date_updated'] = degree.css('p::text').extract()[2]

          # Find index of table and scrape courses
          courses = degree.css('tbody')[index]
          degItem['groups'] = []
          degItem['courses'] = []
          for row in courses.css('tr'):
            course_code = row.xpath('td[1]//text()').extract_first()
            units = row.xpath('td[3]//text()').extract_first()

            if course_code.startswith("A minimum of"):
              # start a new grouping
              self.groupNum += 1
              degItem['groups'].append({
                'group_num': self.groupNum,
                'units': row.xpath('td[2]//text()').extract_first()
              })

            elif course_code.startswith("Total Units"):
              degItem['total_units'] = units

            elif "or" in course_code and len(degItem['courses']) != 0:
              print("appending or course")
              degItem['courses'][-1]["course_code"] += course_code

            else:
              degItem['courses'].append({
                "course_code": course_code,
                "units": units,
                "group": self.groupNum }
              )

          yield degItem

        self.currentIndex += 1
        print(self.currentIndex)

        next_dept_url = self.dept_urls[0][self.currentIndex]
        next_url = response.urljoin(next_dept_url)
        if next_url:
          yield scrapy.Request(next_url, self.parse)


    # def scrape_degree(self, degree_names, degree):
    #   print("SCRAPING DEGREE REQUIREMENTS")

