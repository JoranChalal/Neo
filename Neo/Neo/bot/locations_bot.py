from scrapy.crawler import CrawlerProcess
from Neo.Neo.spiders.locations_href import LocationsHrefSpider
import random

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
]


def get_random_agent():
    return random.choice(user_agent_list)


def scrape_locations_href():

    user_agent = get_random_agent()
    print(user_agent)

    c = CrawlerProcess({
        "USER_AGENT": user_agent,
        "RETRY_HTTP_CODES": [403, 301],
        "RETRY_TIMES": 2,
        "ROBOTSTXT_OBEY": False,
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "CONCURRENT_REQUESTS_PER_IP": 1,
        "COOKIES_ENABLED": False
    })

    c.crawl(LocationsHrefSpider, ["94700,93160,77400",
                                  "2",  # real estate type
                                  "1",  # furnished
                                  "0",  # min price
                                  "2000",  # max price
                                  "1",  # min room
                                  "10",  # max room
                                  "0",  # min square
                                  "250",  # max square
                                  "1"])  # page
    c.start()


scrape_locations_href()
