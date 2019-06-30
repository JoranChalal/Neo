import scrapy
from bs4 import BeautifulSoup
from scrapy.http.request import Request
from Neo.Neo.database.db import insert_locations_data
from datetime import datetime
import cssutils


class LocationsDataSpider(scrapy.Spider):

    name = 'locations_data'
    allowed_domains = ['leboncoin.fr']
    prefix_url = "https://www.leboncoin.fr"

    start_urls = []

    def __init__(self,
                 args="",
                 **kwargs):

        # add href to start_urls
        for item in args[1]:
            self.start_urls.append((self.prefix_url + item["href"])[:])

        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={'full_url': url})

    def parse(self, response):
        # use lxml to get decent HTML parsing speed
        soup = BeautifulSoup(response.text, 'lxml')
        # all data
        title = LocationsDataSpider.get_location_title(soup)
        price = LocationsDataSpider.get_location_price(soup)
        date = LocationsDataSpider.get_location_date(soup)
        description = LocationsDataSpider.get_location_description(soup)
        charges_included = LocationsDataSpider.get_location_charges_included(soup)
        real_estate_type = LocationsDataSpider.get_location_real_estate_type(soup)
        rooms = LocationsDataSpider.get_location_rooms(soup)
        square = LocationsDataSpider.get_location_square(soup)
        images = LocationsDataSpider.get_location_images(soup)
        full_url = str(response.meta['full_url'])

        insert_locations_data({"scraping_date": datetime.now(),
                               "title": title,
                               "price": price,
                               "date": date,
                               "description": description,
                               "charges_included": charges_included,
                               "real_estate_type": real_estate_type,
                               "rooms": rooms,
                               "square": square,
                               "images": images,
                               "full_url": full_url})

        print({"scraping_date": datetime.now(),
                               "title": title,
                               "price": price,
                               "date": date,
                               "description": description,
                               "charges_included": charges_included,
                               "real_estate_type": real_estate_type,
                               "rooms": rooms,
                               "square": square,
                               "images": images,
                               "full_url": full_url})

    @staticmethod
    def get_location_title(html):
        for item in html.findAll("div", {"data-qa-id": "adview_title"}):
            title = item.h1
            if title != "" and title is not None and title.get_text() != "":
                print("Title : " + title.get_text())
                return title.get_text()

    @staticmethod
    def get_location_price(html):
        for item in html.findAll("div", {"data-qa-id": "adview_price"}):
            price = item.span
            if price != "" and price is not None and price.get_text() != "":
                print("Price : " + price.get_text())
                return price.get_text().split()[0]

    @staticmethod
    def get_location_date(html):
        for item in html.findAll("div", {"data-qa-id": "adview_date"}):
            if item != "" and item is not None and item.get_text() != "":
                print("Date : " + item.get_text())
                return datetime.strptime(item.get_text().split()[0], '%d/%m/%Y').strftime("%Y-%m-%d")

    @staticmethod
    def get_location_description(html):
        for item in html.findAll("div", {"data-qa-id": "adview_description_container"}):
            item = item.span
            if item != "" and item is not None and item.get_text() != "":
                print("Description : " + item.get_text())
                return item.get_text()

    @staticmethod
    def get_location_charges_included(html):
        for item in html.findAll("div", {"data-qa-id": "criteria_item_charges_included"}):
            item = item.div
            for div in item:
                if div.get_text() != "Charges comprises" and div != "" and div is not None and div.get_text() != "":
                    print("Charges comprises : " + div.get_text())
                    if div.get_text() == "Oui":
                        return True
                    else:
                        return False

    @staticmethod
    def get_location_real_estate_type(html):
        for item in html.findAll("div", {"data-qa-id": "criteria_item_real_estate_type"}):
            item = item.div
            for div in item:
                if div.get_text() != "Type de bien" and div != "" and div is not None and div.get_text() != "":
                    print("Type de bien : " + div.get_text())
                    options = {"Maison": 1,
                               "Appartement": 2,
                               "Terrain": 3,
                               "Parking": 4,
                               "Autre": 5,
                              }
                    return options[div.get_text()]

    @staticmethod
    def get_location_rooms(html):
        for item in html.findAll("div", {"data-qa-id": "criteria_item_rooms"}):
            item = item.div
            for div in item:
                if div.get_text() != "Pièces" and div != "" and div is not None and div.get_text() != "":
                    print("Pièces : " + div.get_text())
                    return int(div.get_text())

    @staticmethod
    def get_location_square(html):
        for item in html.findAll("div", {"data-qa-id": "criteria_item_square"}):
            item = item.div
            for div in item:
                if div.get_text() != "Surface" and div != "" and div is not None and div.get_text() != "":
                    print("Surface : " + div.get_text())
                    return int(div.get_text().split()[0])

    @staticmethod
    def get_location_images(html):
        urls = ""
        for item in html.findAll("span", {"data-qa-id": "slideshow_thumbnails_item"}):
            item = item.div
            div_style = item['style']
            style = cssutils.parseStyle(div_style)
            url = style['background-image']
            if url != '' and url != "" and url is not None and url != ',' and len(url) > 0:
                if urls == "":
                    urls = url[4:-1]
                else:
                    urls += "|" + url[4:-1]

        for i in range(100):
            urls = urls.replace("||", "|")

        if urls != "":
            if urls[-1:] == "|":
                urls = urls[:-1]

        print(urls)
        return urls