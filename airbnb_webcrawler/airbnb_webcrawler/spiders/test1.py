from scrapy import Spider
from scrapy.selector import Selector
from airbnb_webcrawler.items import AirbnbWebcrawlerItem

class MySpider(Spider):
	name = "airbnb1"
	allowed_domains = ['www.airbnb.com.ec']
	start_urls = ['https://www.airbnb.com.ec/rooms/5914331?s=9eA_J0IH']

	def parse(self, response):

		item2 = AirbnbWebcrawlerItem()
		#inside_room = Selector(response).xpath('//div[@class="expandable-content expandable-content-long"]/div')
		#parrafo = []
		#if inside_room:
		#	for room in inside_room:
		#		item2 = AirbnbWebcrawlerItem()
		#
		#		descripcion = room.xpath('p')
				
		#		for p in descripcion:
		#			aux = p.xpath('span/text()').extract()[0]
		#			parrafo.append(aux)

		reviews_count = Selector(response).xpath('//h4[@class="text-center-sm col-middle col-md-12"]')

		if reviews_count:
			count_review = reviews_count.xpath('span/text()').extract()[0]
			print count_review
		else:
			print 'no reviews'


