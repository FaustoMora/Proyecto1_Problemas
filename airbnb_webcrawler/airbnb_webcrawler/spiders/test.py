from scrapy import Spider, Request
from scrapy.selector import Selector
from airbnb_webcrawler.items import AirbnbWebcrawlerItem

def generar_urls():
	valor_min = [10,51,101,201,301,401,501,601,701,801,901]
	valor_max = [50,100,200,300,400,500,600,700,800,900,1000]
	urls=[]

	for x in range(0,11):
		url = 'https://www.airbnb.com.ec/s/London--United-Kingdom?price_min='+str(valor_min[x])+'&price_max='+str(valor_max[x])+'&ss_id=vgev4c7y'
		urls.append(url)

	return urls


class MySpider(Spider):
	name = "airbnb"
	allowed_domains = ['www.airbnb.com.ec']
	start_urls = generar_urls()

	def parse(self, response):

		rooms = Selector(response).xpath('//div[@class="col-sm-12 row-space-2 col-md-6"]')

		if rooms:
			i=0
			for room in rooms:
				item = AirbnbWebcrawlerItem()

				item['data_id'] = room.xpath('div[@class="listing"]/@data-id').extract()[0]
				item['data_name'] = room.xpath('div[@class="listing"]/@data-name').extract()[0]
				item['data_user'] = room.xpath('div[@class="listing"]/@data-user').extract()[0]
				item['data_lat'] = room.xpath('div[@class="listing"]/@data-lat').extract()[0]
				item['data_lng'] = room.xpath('div[@class="listing"]/@data-lng').extract()[0]
				link = room.xpath('div[@class="listing"]/@data-url').extract()[0]
				item['data_url'] = room.xpath('div[@class="listing"]/@data-url').extract()[0]
				request = Request("https://www.airbnb.com.ec"+link ,callback=self.parse_model, meta={'item':item})
				i = i +1
				print i
				yield request


	def parse_model(self, response):
		print 'dentro de la habitacion'

		inside_room = Selector(response).xpath('//div[@class="expandable-content expandable-content-long"]/div')

		if inside_room:
			for room in inside_room:
				item = AirbnbWebcrawlerItem(response.meta["item"])

				descripcion = room.xpath('p')

				parrafo = []
				for p in descripcion:
					aux = p.xpath('span/text()').extract()[0]
					parrafo.append(aux)

				item['data_descripcion'] = ' '.join(parrafo)
				yield item

	def parse_users(self,response):
		print 'dentro de los usuarios'








