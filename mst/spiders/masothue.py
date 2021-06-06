import scrapy
from scrapy_splash import SplashRequest
from mst.items import MstItem


class MstCrawlSpider(scrapy.Spider):
    name = 'masothue'
    allowed_domains = ['masothue.com']
    start_urls = ['https://masothue.com/0106128881-002-chi-nhanh-cong-ty-co-phan-thuong-mai-va-giao-duc-nhat-han-quang-binh',
                  'https://masothue.com/6001717390-cong-ty-tnhh-xay-dung-va-thiet-bi-tay-nguyen']

    render_script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(0))

            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url,
                self.parse,
                endpoint='render.html',
                args={
                    'wait': 0,
                    'lua_source': self.render_script,
                }
            )

    def parse(self, response):
        item = MstItem()

        for product in response.css("table.table-taxinfo"):
            item["name"] = product.css("th > span ::text").get()
            item["alternateName"] = product.css("tr td[itemprop='alternateName'] > span ::text").get()
            item["taxID"] = product.css("tr td[itemprop='taxID'] > span ::text").get()
            item["address"] = product.css("tr td[itemprop='address'] > span ::text").get()
            item["telephone"] = product.css("tr td[itemprop='telephone'] > span ::text").get()

            yield item