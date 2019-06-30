from scrapy.crawler import CrawlerProcess
from Neo.Neo.spiders.locations_href import LocationsHrefSpider
from Neo.Neo.spiders.locations_data import LocationsDataSpider
from Neo.Neo.database.db import get_all_locations_href, get_all_postal_code, get_94_postal_codes
from scrapy.utils.project import get_project_settings
import random

c = CrawlerProcess({
    'RETRY_HTTP_CODES': [403, 301],
    'RETRY_TIMES': 12,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 50,
    'CONCURRENT_REQUESTS_PER_IP': 50,
    'CONCURRENT_REQUESTS': 50,
    'PROXY_POOL_ENABLED': True,
    'HTTPCACHE_ENABLED': True,
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
        'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    },
    'ROBOTSTXT_OBEY': False,
    #'DOWNLOAD_DELAY': 0,
    #'RANDOMIZE_DOWNLOAD_DELAY': 0,
    'COOKIES_ENABLED': False
})


def crawl_locations_href(postal_code_list):

    c.crawl(LocationsHrefSpider, [",".join(postal_code_list),
                                  "2",  # real estate type
                                  "1",  # furnished
                                  "0",  # min price
                                  "2000",  # max price
                                  "1",  # min room
                                  "10",  # max room
                                  "0",  # min square
                                  "250",  # max square
                                  "1"])  # page


def crawl_locations_data(postal_code_list):
    for postal_code in postal_code_list:
        href_dict = get_all_locations_href(postal_code)
        c.crawl(LocationsDataSpider, [postal_code, href_dict])


def run_crawler():
    #crawl_locations_href(get_94_postal_codes())
    crawl_locations_data(get_94_postal_codes())
    c.start()


run_crawler()
