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

		reviews_room = Selector(response).xpath('//div[@class="row review"]')
		print len(reviews_room)
		
		if reviews_room:
			for review in reviews_room:
				print review.xpath('a[@class="media-photo media-round"]/@href').extract()[0]		
		else:
			print 'no reviews_room'

		#item2['data_descripcion'] = ' '.join(parrafo)
		yield item2


