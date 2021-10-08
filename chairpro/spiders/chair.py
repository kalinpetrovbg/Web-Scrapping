import scrapy


class ChairSpider(scrapy.Spider):
    name = 'chair'
    allowed_domains = ['www.chairpro.bg/']
    start_urls = 'https://www.chairpro.bg/collections/ergonomichni-stolove'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls,
                             callback=self.parse,
                             headers={"User-Agent": self.user_agent}
                             )

    def parse(self, response, **kwargs):
        product = response.xpath('//div[@class="product-thumb"]')

        for each in product:
            name = each.xpath('.//div/h5/text()').get()
            price = each.xpath('.//div/ul/li/span/text()').get()
            link = each.xpath('.//@href').get()

            yield {
                "name": name,
                "price": price,
                "link": link,
            }
