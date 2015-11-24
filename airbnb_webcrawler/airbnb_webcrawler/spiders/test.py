from scrapy import Spider
from scrapy.selector import Selector
from airbnb_webcrawler.items import AirbnbWebcrawlerItem

class MySpider(Spider):
	name = "airbnb"
	allowed_domains = ['https://www.airbnb.com.ec/']
	start_urls = ['https://www.airbnb.com.ec/s/London--United-Kingdom?ss_id=vgev4c7y']

	def parse(self, response):

		rooms = Selector(response).xpath('//div[@class="col-sm-12 row-space-2 col-md-6"]')

		if rooms:
			for room in rooms:
				item = AirbnbWebcrawlerItem()

				item['data_name'] = room.xpath('div[@class="listing"]/@data-name').extract()[0]
				item['data_user'] = room.xpath('div[@class="listing"]/@data-user').extract()[0]
				item['data_lat'] = room.xpath('div[@class="listing"]/@data-lat').extract()[0]
				item['data_lng'] = room.xpath('div[@class="listing"]/@data-lng').extract()[0]
				link = room.xpath('div[@class="listing"]/@data-url').extract()[0]
				item['data_url'] = room.xpath('div[@class="listing"]/@data-url').extract()[0]
				
				#impresiones
				print 'name: ' + item['data_name']
				print 'lat:' + item['data_lat'] + ' lng:' + item['data_lng']



