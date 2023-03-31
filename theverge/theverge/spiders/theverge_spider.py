import sqlite3
from scrapy.crawler import CrawlerProcess
from datetime import date
from scrapy import Spider
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from theverge.settings import CHROMEDRIVER_PATH, THEVERGE_URL
import os
import datetime


class TheVergeSpider(Spider):
    name = "com.theverge"
    start_urls = [THEVERGE_URL]
    handle_httpstatus_list = [404]
    
    def __init__(self):
        self.baseURL = "https://www.theverge.com"
        driver_path = CHROMEDRIVER_PATH
        self.id =0
        options = Options()
        options.add_argument('--headless')
        self.driver = Chrome(executable_path=driver_path,
                             options=options)
        self.conn = sqlite3.connect('theverge.db')
        self.create_table()
    
    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS articles
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             url TEXT,
                             headline TEXT,
                             author TEXT,
                             date TEXT);''')

    def insert_article(self, url, headline, author, date):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE url=?', (url,))
        result = cursor.fetchone()
        if result:
            return;
        sql = f"INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)"
        self.conn.execute(sql, (url, headline, author, date))
        self.conn.commit()
    
    @classmethod
    def find_DMY(self):
        today = datetime.date.today()
        date_str = today.strftime('%d%m%Y')
        return date_str + '_verge.csv'

    def insert_headerSection(self, response):
        
        div_tags = response.css(
            'div[class*="relative border-b border-gray-31 pb-20 md:pl-80 lg:border-none lg:pl-[165px] -mt-20 sm:-mt-40"]')

        # Do something with the extracted data, such as storing it in an item or printing it
        yield {
            'id':self.id,
            'URL': self.baseURL+div_tags.css('a::attr(href)').get(),
            'headline': div_tags.css('h2 a::text').get(),
            'author': div_tags.css('div[class="inline-block"] a::text').get(),
            'date': div_tags.css('div[class="inline-block"] span::text').get()
        }
        self.insert_article(self.baseURL+div_tags.css('a::attr(href)').get(), div_tags.css('h2 a::text').get(), div_tags.css('div[class="inline-block"] a::text').get(), div_tags.css('div[class="inline-block"] span::text').get())
        self.id+=1

    # Inserting sideSection
    def insert_sideSection(self, response):

        div_tags = response.css(
            'div[class*="max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10"]')

        # Pusing the sideBar 5 headlines
        for div in div_tags:
            url = div.css('a::attr(href)').get()
            headline = div.css('h2 a::text').get()
            author = div.css('div[class="inline-block"] a::text').get()
            date = div.css('div[class="inline-block"] span::text').get()

            yield {
                'id':self.id,
                'URL': self.baseURL+url,
                'headline': headline,
                'author': author,
                'date': date
            }
            self.insert_article(url, headline, author, date)
            self.id+=1

    # Inserting mainSection
    def insert_mainSection(self, response):

        div_tags = response.css('div.max-w-content-block-mobile')

        # Pusing the mainSection 30 headlines
        for div in div_tags:
            headline = div.css('h2 a::text').get()

            if (headline == "Advertiser Content"):
                continue
            
            url = div.css('a[class*="after:absolute after:inset-0 group-hover:shadow-underline-blurple dark:group-hover:shadow-underline-franklin"]::attr(href)').get()
            author = div.css('div[class="inline-block"] a::text').get()
            date = div.css('div[class="inline-block"] span::text').get()

          # Do something with the extracted data, such as storing it in an item or printing it
            yield {
                'id':self.id,
                'URL': self.baseURL+url,
                'headline': headline,
                'author': author,
                'date': date
            }
            self.insert_article(url, headline, author, date)
            self.id+=1

    def parse(self, response):
        
        if response.status == 404:
            self.logger.error("404 error: Page not found: %s", response.url)
            return
        
        self.driver.get(response.url)
        body = self.driver.page_source.encode('utf-8')
        response_sel = Selector(text=body)

        yield from self.insert_headerSection(response_sel)
        yield from self.insert_sideSection(response_sel)
        yield from self.insert_mainSection(response_sel)


# Getting the csv file name
obj = TheVergeSpider()
csv_name = obj.find_DMY()

csv_path = os.path.join('saved_csv_files\\',csv_name)
if os.path.exists(csv_path):
    os.remove(csv_path)

process = CrawlerProcess(settings={
    "FEEDS": {
        csv_path: {"format": "csv", "encoding": "utf-8"},
    },
})
