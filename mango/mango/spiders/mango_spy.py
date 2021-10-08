import scrapy
from scrapy_splash import SplashRequest


class MangSpySpider(scrapy.Spider):
    name = "mango-spy"
    allowed_domains = ["www.mango.com/"]
    url = "https://shop.mango.com/bg-en/women/skirts-midi/midi-satin-skirt_17042020.html?c=99"

    script = """
    function main(splash, args)
        splash:set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36')
        splash.private_mode_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(1))
        splash:set_viewport_full()
        return {splash:html()}
    end
    """

    def start_requests(self):
        yield SplashRequest(url=self.url,
                            callback=self.parse,
                            endpoint="execute",
                            args={"lua_source": self.script,
                                  }
                            )

    def parse(self, response, **kwargs):
        name = response.xpath('//h1/text()').get()
        prices = response.xpath('//span[contains(@class, "product-sale" )]/text()').getall()
        selected_color = response.xpath('//div[contains(@class, "color-container")]/img/@alt').get()
        sizes = response.xpath('//div[contains(@class, "selector")]/div/span/@data-size').getall()

        """ PRICE
        When there are regular and sale price, 'prices' has two elements.
        We take only the last element, which is the current selling price.
        Then with replace() function we remove the currency abbreviation "лв."."""
        price = prices[-1].replace("\\u043b\\u0432.", "")

        """ COLOR
        Delete unnecessary symbols from the selected color """
        color = selected_color[2:-2]

        """ SIZE
        Delete unnecessary symbols from each of the size types """
        size = []
        for each in sizes:
            size.append(each[2:-2])

        yield {
            "name": name,
            "price": float(price),
            "color": color,
            "size": size,
        }
