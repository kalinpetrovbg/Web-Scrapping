import scrapy
# from scrapy_splash import SplashRequest
import logging


class AntaresSpider(scrapy.Spider):
    name = 'antares'
    allowed_domains = ['www.antares-bg.net']
    start_urls = ['https://antares-bg.net/ofis-stolove-ceni']

    # url = "https://antares-bg.net/ofis-stolove-ceni"
    #
    # script = '''
    # function main(splash, args)
    #     splash:set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36')
    #     splash.private_mode_enabled = false
    #     assert(splash:go(args.url))
    #     assert(splash:wait(1))
    #     splash:set_viewport_full()
    #     return {splash:html()}
    # end
    # '''
    # def start_requests(self):
    #     yield SplashRequest(url=self.url,
    #                         callback=self.parse,
    #                         endpoint='execute',
    #                         args={'lua_source': self.script})

    def parse(self, response, **kwargs):
        domain = "https://antares-bg.net"
        elements = response.xpath('//li[@class="col-md-4 product_list"]')
        for e in elements:
            name = e.xpath('.//a/@title').get()
            link = e.xpath('.//a/@href').get()
            price = e.xpath('.//div[@class="standardh3 price_top"]/text()').getall()
            corrected_price = price[-1][5:]

            yield {
                "name": name,
                "price": corrected_price,
                "link": f"{domain}{link}",
            }
