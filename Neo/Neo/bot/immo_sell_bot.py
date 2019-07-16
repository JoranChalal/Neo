from scrapy.crawler import CrawlerProcess
from Neo.Neo.spiders.immo_sell_href import ImmoSellHrefSpider
from Neo.Neo.spiders.immo_data import ImmoDataSpider
from Neo.Neo.database.database import Property, get_postal_codes

c = CrawlerProcess({
    'RETRY_HTTP_CODES': [404, 403, 301],
    'RETRY_TIMES': 10,
    'DOWNLOAD_TIME': 5,
    'AUTOTHROTTLE_ENABLED': False,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
    'CONCURRENT_REQUESTS_PER_IP': 32,
    'CONCURRENT_REQUESTS': 32,
    'PROXY_POOL_ENABLED': True,
    'HTTPCACHE_ENABLED': False,
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
        'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    },
    'ROBOTSTXT_OBEY': False,
    #'RANDOMIZE_DOWNLOAD_DELAY': 0,
    'COOKIES_ENABLED': False,
})


def crawl_immo_sell_href(postal_code_list):

    c.crawl(ImmoSellHrefSpider, [",".join(postal_code_list),
                                  "2",  # real estate type
                                  "0",  # min price
                                  "1000000",  # max price
                                  "1",  # min room
                                  "10",  # max room
                                  "0",  # min square
                                  "1000",  # max square
                                  "1"])  # page

def crawl_locations_data(postal_code_list):
    for postal_code in postal_code_list:
        # get all href as dictionary
        properties_list = (Property.select().where(Property.postal_code == postal_code))
        href_list = []
        for property in properties_list:
            # Only parse failed one and new one
            if property.title == "":
                print(property.full_url)
                href_list.append(property.full_url)

        if len(href_list) > 0:
            c.crawl(ImmoDataSpider, [postal_code, href_list])


def run_crawler():
    #crawl_immo_sell_href(get_postal_codes())
    crawl_locations_data(get_postal_codes())
    c.start()


run_crawler()
