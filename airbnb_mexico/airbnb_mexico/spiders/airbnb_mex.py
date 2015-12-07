# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from selenium import webdriver
from airbnb_mexico.items import AirbnbMexicoItem


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
        for r in rooms:
            yield Request(r.url,callback=self.parse_room)
    #a = Request('https://www.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=es&listing_id=2701524&role=guest&_format=for_p3&_limit=50&_offset=14&_order=language')

    def parse_room(self,response):
        item = AirbnbMexicoItem()
        item['id'] = response.url.split('/')[-1].split('?')[0]
        item['latitud'] = response.xpath('/html/head/meta[18]/@content').extract()[0]
        item['longitud'] = response.xpath('/html/head/meta[19]/@content').extract()[0]
        item['nombre']=response.xpath('//title/text()').extract()[0]
        item['ubicacion']=response.xpath('//div[@id="display-address"]/a[1]/text()').extract()[0]
        item['costo']=response.xpath('//div[@class="book-it__price js-price"]/div[@class="book-it__price-amount js-book-it-price-amount pull-left h3 text-special"]/text()').extract()[0].strip().replace('$','')
        item['acomodados']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Accommodates")]/text()').extract()[0]
        item['banios']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bathrooms")]/text()').extract()[0]
        item['cama_tipo']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bed t")]/text()').extract()[0]
        item['cuartos']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bedrooms")]/text()').extract()[0]
        item['camas']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Beds")]/text()').extract()[0]
        item['check_in']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Check In")]/text()').extract()[0]
        item['check_out']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Check Out")]/text()').extract()[0]
        item['tipo_propiedad']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Property type")]/text()').extract()[0]
        item['tipo_habitacion']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Room type")]/text()').extract()[0]
        #item['servicios']=';'.join(response.xpath('//div[@class="row"]//div[@class="space-1"]/span[2]/text()').extract())


    def parse_room_servicios(self,response):
        item = response.meta['item']