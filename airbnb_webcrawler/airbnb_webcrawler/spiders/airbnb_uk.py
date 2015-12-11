# -*- coding: utf-8 -*-

from pyvirtualdisplay import Display


import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from selenium import webdriver
from scrapy.linkextractors import LinkExtractor
from airbnb_webcrawler.items import AirbnbUKItem
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait

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
            url = 'https://www.airbnb.com.ec/s/uk?price_min='+str(valores_minimos[x])+'&price_max='+str(valores_maximos[x])+'&ss_id=vgev4c7y&page='+str(y)
            urls.append(url)

    return urls

class AirbnbUKSpider(scrapy.Spider):
    name = "airbnb-uk"
    allowed_domains = ["airbnb.com","www.airbnb.com"]
    start_urls = generar_urls()

    extract_rooms = LinkExtractor(allow=r'/rooms/\d+')
    extract_pages = LinkExtractor(allow=r'/s/uk\?page=\d+',restrict_xpaths='//li[@class="next next_page"]')

    def __init__(self):
        user_agent = (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36'
        )
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = user_agent
        self.driver = webdriver.Firefox()


    def parse(self, response):
        rooms = self.extract_rooms.extract_links(response)
        pages = self.extract_pages.extract_links(response)
        for r in rooms:
            yield Request(r.url,callback=self.parse_room)
    #a = Request('https://www.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=USD&locale=es&listing_id=2701524&role=guest&_format=for_p3&_limit=50&_offset=14&_order=language')

    def parse_room(self,response):
        self.driver.get(response.url)
        #mores = self.driver.find_element_by_class_name()
        mores = self.driver.find_elements_by_class_name('expandable-trigger-more')
        for m in mores:
            m.click()
        item = AirbnbUKItem()
        try:
            item['id'] = response.url.split('/')[-1].split('?')[0]
        except:
            item['id'] = ""
        try:
            item['latitud'] = response.xpath('/html/head/meta[18]/@content').extract()[0]
        except:
            item['latitud']=""
        try:
            item['longitud'] = response.xpath('/html/head/meta[19]/@content').extract()[0]
        except:
            item['longitud']
        try:
            item['nombre']=response.xpath('//title/text()').extract()[0]
        except:
            item['nombre']=""
        try:
            item['ubicacion']=response.xpath('//div[@id="display-address"]/a[1]/text()').extract()[0]
        except:
            item['ubicacion']=""
        try:
            item['costo']=response.xpath('//div[@class="book-it__price js-price"]/div[@class="book-it__price-amount js-book-it-price-amount pull-left h3 text-special"]/text()').extract()[0].strip().replace('$','')
        except:
            item['costo']=""
        try:
            item['acomodados']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Accommodates")]/text()').extract()[0]
        except:
            item['acomodados']=""
        try:
            item['banios']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bathrooms")]/text()').extract()[0]
        except:
            item['banios']=""
        try:
            item['cama_tipo']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bed t")]/text()').extract()[0]
        except:
            item['cama_tipo']=""
        try:
            item['cuartos']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Bedrooms")]/text()').extract()[0]
        except:
            item['cuartos']=""
        try:
            item['camas']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Beds")]/text()').extract()[0]
        except:
            item['camas']=""
        try:
            item['check_in']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Check In")]/text()').extract()[0]
        except:
            item['check_in']=""
        try:
            item['check_out']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Check Out")]/text()').extract()[0]
        except:
            item['check_out']=""
        try:
            item['tipo_propiedad']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Property type")]/text()').extract()[0]
        except:
            item['tipo_propiedad']=""
        try:
            item['tipo_habitacion']=response.xpath('//div[@class="row"]/div[@class="col-md-9"]/div[@class="row"]//strong[contains(@data-reactid,"Room type")]/text()').extract()[0]
        except:
            item['tipo_habitacion']
        #item['servicios']=';'.join(response.xpath('//div[@class="row"]//div[@class="space-1"]/span[2]/text()').extract())
        servicios = self.driver.find_elements_by_xpath('//div[@class="row"]//div[@class="space-1"]//strong')
        item['servicios'] = []
        for s in servicios:
            item['servicios'].append(s.text)
        item['servicios'] = ';'.join(item['servicios'])
        item['descripcion'] = '\n'.join(response.xpath('//div[@class="react-expandable"]/div[@class="expandable-content expandable-content-long"]//p/span/text()').extract())
        item['reglas'] = '\n'.join(response.xpath('//div[@id="house-rules"]//p/span/text()').extract())
        reviews_pages = self.driver.find_elements_by_xpath('//div[@class="pagination pagination-responsive"]//li[@class!="next next_page"]/a')
        item['reviews']=[]
        for r in reviews_pages:
            r.click()
            self.driver.implicitly_wait(3)
            reviews = self.driver.find_elements_by_xpath('//div[@class="review-text"]//p')
            for rev in reviews:
                item['reviews'].append(rev.text)



        item['reviews'] = '\n'.join(item['reviews'])


        print item['reviews']



