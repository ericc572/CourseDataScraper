# Scrapy scripts for course scraping
## Usage for PDF scraping
- First, download PDF from: https://assist.org/transfer/report/24086477
- Convert pdf to txt: 
`$  pdf2txt.py transfer_reports/another_assist.pdf >>
     transfer_reports/solano.txt`
- Run my python script: `$ python pdf_reader.py transfer_reports/solano.txt OUTPUT_FILE.csv`

## Usage:
- `cd course_scraper`
- `scrapy crawl degree_spider -o data.json`
- [optional: pretty format] `jq '.' data.json >> another_file_name.json`

To launch a shell env: `scrapy shell https://www.scc.losrios.edu/2020-2021-catalog/programs-of-study/list-of-programs/accounting`
