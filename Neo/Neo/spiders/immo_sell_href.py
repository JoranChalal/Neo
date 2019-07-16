import scrapy
from bs4 import BeautifulSoup
from scrapy.http.request import Request
from Neo.Neo.database.database import Property


class ImmoSellHrefSpider(scrapy.Spider):

    name = 'locations_href'
    allowed_domains = ['leboncoin.fr']
    immo_href = []
    start_urls = []

    def __init__(self,
                 args="",
                 **kwargs):

        postal_code_list = args[0].split(",")

        self.url_prefix = "https://www.leboncoin.fr"

        for postal_code in postal_code_list:
            self.url_query_pages = "/recherche/?category=" + "9" + \
                              "&locations=" + postal_code + \
                              "&immo_sell_type=old,new" + \
                              "&real_estate_type=" + args[1] + \
                              "&price=" + args[2] + "-" + \
                              args[3] + \
                              "&rooms=" + args[4] + "-" + args[5] + \
                              "&square=" + args[6] + "-" + args[7] + \
                              "&page=" + args[8]
            self.start_urls.append(self.url_prefix + self.url_query_pages)
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={'postal_code': url.split("&locations=")[1][:5],
                                                    'full_url': url})

    def parse(self, response):
        # use lxml to get decent HTML parsing speed
        soup = BeautifulSoup(response.text, 'lxml')

        old_immo_list = list(Property.select().where(Property.postal_code == response.meta['postal_code']))
        old_immo_href_list = []
        for item in old_immo_list:
            old_immo_href_list.append(item.full_url)

        items_count = len(soup.findAll("a", {"class": "clearfix trackable"}))

        for item in soup.findAll("a", {"class": "clearfix trackable"}):
            if not self.url_prefix + item["href"] in old_immo_href_list:
                tmp_dict = {"href": item["href"], "visited": False}
                self.immo_href.append(tmp_dict)
                Property.insert(full_url=self.url_prefix + item["href"],
                                postal_code=response.meta['postal_code']).on_conflict('replace').execute()

        if items_count > 0:
            url_dict = {response.meta['postal_code']: self.immo_href}
            # Request next page if there are results in this one
            next_page = int(float(response.meta['full_url'][-1:])) + 1
            yield self.make_requests_from_url(response.meta['full_url'][:-1] + str(next_page))

        # clear
        self.immo_href = []


def is_href_in_dict(href_dict, href):
    for item in href_dict:
        if item["href"] == href:
            return True
    return False
