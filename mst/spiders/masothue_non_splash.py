import scrapy
from mst.items import MstItem
from scrapy.linkextractors import LinkExtractor

class MstCrawlSpider(scrapy.Spider):
    name = 'masothue_non_splash'
    allowed_domains = ['masothue.com']
    start_urls = ['https://masothue.com/0106128881-002-chi-nhanh-cong-ty-co-phan-thuong-mai-va-giao-duc-nhat-han-quang-binh',
                  'https://masothue.com/6001717390-cong-ty-tnhh-xay-dung-va-thiet-bi-tay-nguyen']

    def start_requests(self):
        dem = 0
        for url in self.start_urls:
            dem = dem + 1
            if dem > 10:
                break
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = MstItem()
        for product in response.css("table.table-taxinfo"):
            item["name"] = product.css("th > span ::text").get()
            item["alternateName"] = product.css("tr td[itemprop='alternateName'] > span ::text").get()
            item["taxID"] = product.css("tr td[itemprop='taxID'] > span ::text").get()
            item["address"] = product.css("tr td[itemprop='address'] > span ::text").get()
            item["telephone"] = product.css("tr td[itemprop='telephone'] > span ::text").get()
            yield item
