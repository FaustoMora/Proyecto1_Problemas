# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request


class AirbnbMexSpider(scrapy.Spider):
    name = "airbnb-mex"
    allowed_domains = ["airbnb.com","www.airbnb.com"]
    start_urls = (
        'http://www.airbnb.com/s/mexico',
    )
    extract_rooms = SgmlLinkExtractor(allow=r'/rooms/\d+')
    extract_pages = SgmlLinkExtractor(allow=r'/s/mexico\?page=\d+')

    def parse(self, response):
        rooms = self.extract_rooms.extract_links(response)
        pages = self.extract_pages.extract_links(response)
        a = Request('https://www.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=es&listing_id=2701524&role=guest&_format=for_p3&_limit=50&_offset=14&_order=language')
        print a.
