from theverge.spiders import theverge_spider
from theverge.spiders.theverge_spider import process

if __name__ =='__main__':
    process.crawl(theverge_spider.TheVergeSpider)
    process.start()