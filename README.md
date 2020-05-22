# Scrapy scripts for course scraping

## Usage:
- cd course_scraper
- scrapy crawl degree_spider -o data.json
- [optional: pretty format] jq '.' data.json >> another_file_name.json

To launch a shell env: scrapy shell https://www.scc.losrios.edu/2020-2021-catalog/programs-of-study/list-of-programs/accounting
