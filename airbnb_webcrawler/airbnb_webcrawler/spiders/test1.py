from scrapy import Spider
from scrapy.selector import Selector
from airbnb_webcrawler.items import AirbnbWebcrawlerItem

class MySpider(Spider):
	name = "airbnb1"
	allowed_domains = ['https://www.airbnb.com.ec/']
	start_urls = ['https://www.airbnb.com.ec/rooms/5914331?s=9eA_J0IH']

	def parse(self, response):

		inside_room = Selector(response).xpath('//div[@class="expandable-content expandable-content-long"]/div')

		if inside_room:
			for room in inside_room:
				item2 = AirbnbWebcrawlerItem()

				descripcion = room.xpath('p')

				parrafo = []
				for p in descripcion:
					aux = p.xpath('span/text()').extract()[0]
					parrafo.append(aux)

				item2['data_descripcion'] = ' '.join(parrafo)
				yield item2


