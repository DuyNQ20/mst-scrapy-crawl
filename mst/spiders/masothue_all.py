import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mst.items import TaxUrls, MstItem
import ast


class MstCrawlSpider(scrapy.Spider):
    name = 'masothue_all'
    allowed_domains = ['masothue.com']
    # start_urls = ['https://masothue.com/tra-cuu-ma-so-thue-theo-tinh/ca-mau-108']
    page_number = 1

    def start_requests(self):
        with open("url.json", "r") as f:
            text = f.read()
            start_urls = ast.literal_eval(text)
        for url in start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        currentPage = response.css("span.page-numbers.current::text").get()
        if int(currentPage) == self.page_number:
            itemUrl = TaxUrls()
            urls = response.css("div[data-prefetch]::attr(data-prefetch)").getall()
            for url in urls:
                itemUrl["url"] = url
                yield itemUrl
            self.page_number = self.page_number + 1
            next_page = "/tra-cuu-ma-so-thue-theo-tinh/ca-mau-108?page=" + str(self.page_number) + ""
            yield response.follow(url=next_page, callback=self.parse)

    # def parse(self, response):
    #     currentPage = response.css("span.page-numbers.current::text").get()
    #     if int(currentPage) == self.page_number:
    #         itemUrl = TaxUrls()
    #         urls = response.css("div[data-prefetch]::attr(data-prefetch)").getall()
    #         yield from response.follow_all(urls, self.getTax)
    #         self.page_number = self.page_number + 1
    #         next_page = "/tra-cuu-ma-so-thue-theo-tinh/ca-mau-108?page=" + str(self.page_number) + ""
    #         next_page = response.urljoin(next_page)
    #         if next_page:
    #             yield scrapy.Request(url=next_page, callback=self.parse)
    #
    # def getTax(self, response):
    #     item = MstItem()
    #     for product in response.css("table.table-taxinfo"):
    #         item["name"] = product.css("th > span ::text").get()
    #         item["alternateName"] = product.css("tr td[itemprop='alternateName'] > span ::text").get()
    #         item["taxID"] = product.css("tr td[itemprop='taxID'] > span ::text").get()
    #         item["address"] = product.css("tr td[itemprop='address'] > span ::text").get()
    #         item["telephone"] = product.css("tr td[itemprop='telephone'] > span ::text").get()
    #         yield item
