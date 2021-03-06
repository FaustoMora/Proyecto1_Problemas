# -*- coding: utf-8 -*-
import os

from pyvirtualdisplay import Display


import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from selenium import webdriver
from scrapy.linkextractors import LinkExtractor
from airbnb_mexico.items import AirbnbMexicoItem
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import time


def quitarCommas(text):
    return text.replace(",", ".")

def generar_urls():
    rango_1 = [i for i in range(10,460)]
    rango_20 = [i for i in range(460,1000,10)]

    valores_maximos=[]
    valores_minimos=[]

    for x in range(0,len(rango_1)):
        if x%2==0:
            valores_maximos.append(rango_1[x+1])
        else:
            valores_minimos.append(rango_1[x-1])

    for x in range(0,len(rango_20)):
        valores_minimos.append(rango_20[x])
        if rango_20[x] != 460:
            valores_maximos.append(rango_20[x]-1)
            
    valores_maximos.append(1000)
    urls=[]

    for x in range(0,len(valores_maximos)):
        for y in range(1,18):
            url = 'http://www.airbnb.com/s/mexico?price_min='+str(valores_minimos[x])+'&price_max='+str(valores_maximos[x])+'&page='+str(y)+'&ss_id=pp5dwaol'
            urls.append(url)

    return urls


class AirbnbMexSpider(scrapy.Spider):
    name = "airbnb-mex"
    download_delay = 0.25
    allowed_domains = ["airbnb.com","www.airbnb.com"]
    start_urls = generar_urls()

    extract_rooms = LinkExtractor(allow=r'/rooms/\d+')
    extract_pages = LinkExtractor(allow=r'/s/mexico\?page=\d+',restrict_xpaths='//li[@class="next next_page"]')

    def __init__(self):
        user_agent = (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
        )
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap["phantomjs.page.settings.userAgent"] = user_agent
        self.driver = None



    def parse(self, response):
        rooms = self.extract_rooms.extract_links(response)
        pages = self.extract_pages.extract_links(response)
        for r in rooms:
            yield Request(r.url,callback=self.parse_room)
    #a = Request('https://www.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=es&listing_id=2701524&role=guest&_format=for_p3&_limit=50&_offset=14&_order=language')

    def parse_room(self,response):
        self.driver = webdriver.PhantomJS(desired_capabilities=self.dcap)
        self.driver.get(response.url)
        time.sleep(3)

        #mores = self.driver.find_element_by_class_name()
        mores = self.driver.find_elements_by_class_name('expandable-trigger-more')
        for m in mores:
            m.click()
            time.sleep(1)
        item = AirbnbMexicoItem()
        try:
            item['id'] = response.url.split('/')[-1].split('?')[0]
        except:
            item['id'] = ""
        try:
            item['latitud'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:latitude"]/@content').extract()[0]
        except:
            item['latitud']="no"
        try:
            item['longitud'] = response.xpath('/html/head/meta[@property="airbedandbreakfast:location:longitude"]/@content').extract()[0]
        except:
            item['longitud']="no"
        try:
            item['nombre']=response.xpath('//title/text()').extract()[0]
            item['nombre']=quitarCommas(item['nombre'])
        except:
            item['nombre']=""
        try:
            item['ubicacion']=response.xpath('//div[@id="display-address"]/a[1]/text()').extract()[0]
            item['ubicacion']=quitarCommas(item['ubicacion'])
        except:
            item['ubicacion']=""
        try:
            item['costo']=response.xpath('//div[@class="book-it__price js-price"]/div[@class="book-it__price-amount js-book-it-price-amount pull-left h3 text-special"]/text()').extract()[0].strip().replace('$','')
        except:
            item['costo']=""
        try:
            item['acomodados']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Accommodates")]/text()').extract()[0]
            item['acomodados']=quitarCommas(item['acomodados'])
        except:
            item['acomodados']=""
        try:
            item['banios']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bathrooms")]/text()').extract()[0]
            item['banios']=quitarCommas(item['banios'])
        except:
            item['banios']=""
        try:
            item['cama_tipo']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bed t")]/text()').extract()[0]
            item['cama_tipo']=quitarCommas(item['cama_tipo'])
        except:
            item['cama_tipo']=""
        try:
            item['cuartos']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bedrooms")]/text()').extract()[0]
            item['cuartos']=quitarCommas(item['cuartos'])
        except:
            item['cuartos']=""
        try:
            item['camas']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Beds")]/text()').extract()[0]
            item['camas']=quitarCommas(item['camas'])
        except:
            item['camas']=""
        try:
            item['check_in']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Check In")]/text()').extract()[0]
            item['check_in']=quitarCommas(item['check_in'])
        except:
            item['check_in']=""
        try:
            item['check_out']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Check Out")]/text()').extract()[0]
            item['check_out']=quitarCommas(item['check_out'])
        except:
            item['check_out']=""
        try:
            item['tipo_propiedad']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Property type")]/text()').extract()[0]
            item['tipo_propiedad']=quitarCommas(item['tipo_propiedad'])
        except:
            item['tipo_propiedad']=""
        try:
            item['tipo_habitacion']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Room type")]/text()').extract()[0]
            item['tipo_habitacion']=quitarCommas(item['tipo_habitacion'])
        except:
            item['tipo_habitacion']=""
        try:
            item['nro_reviews'] = int(response.xpath('//div[@class="review-wrapper"]//h4/span/text()').extract()[0].split(" ")[0])
        except:
            item['nro_reviews'] = ""


        servicios = self.driver.find_elements_by_xpath('//div[@class="row"]//div[@class="space-1"]//strong')
        item['servicios'] = []
        for s in servicios:
            item['servicios'].append(quitarCommas(s.text))

        item['servicios'] = '.'.join(item['servicios'])
        item['servicios'] = quitarCommas(item['servicios'])
        item['descripcion'] = '\n'.join(response.xpath('//div[@class="react-expandable"]/div[@class="expandable-content expandable-content-long"]//p/span/text()').extract())
        item['descripcion'] = quitarCommas(item['descripcion'])
        item['reglas'] = '\n'.join(response.xpath('//div[@id="house-rules"]//p/span/text()').extract())
        item['reglas'] = quitarCommas(item['reglas'])


        # reviews_pages = self.driver.find_elements_by_xpath('//div[@class="pagination pagination-responsive"]//li[@class!="next next_page"]/a')

        # for r in reviews_pages:
        #     r.click()
        #     self.driver.implicitly_wait(3)
        #     reviews = self.driver.find_elements_by_xpath('//div[@class="review-text"]//p')
        #     for rev in reviews:
        #         item['reviews'].append(quitarCommas(rev.text))
        item['reviews']=[]
        review_next = self.driver.find_elements_by_xpath('//div[@class="pagination pagination-responsive"]//li[@class="next next_page"]/a')
        while review_next != None:
            reviews = self.driver.find_elements_by_xpath('//div[@class="review-text"]//p')
            for rev in reviews:
                item['reviews'].append(quitarCommas(rev.text))
            try:
                review_next[0].click()
                time.sleep(2)
                review_next = self.driver.find_elements_by_xpath('//div[@class="pagination pagination-responsive"]//li[@class="next next_page"]/a')
            except:
                review_next=None






        item['reviews'] = ' $$ '.join(item['reviews'])
        item['descripcion'] = quitarCommas(item['descripcion'])
        item['reglas'] = quitarCommas(item['reglas'])

        self.driver.quit()
        os.system('killall -9 phantomjs')

        yield item


