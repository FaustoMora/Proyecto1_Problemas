from scrapy import Spider, Request
from scrapy.selector import Selector
from airbnb_webcrawler.items import AirbnbWebcrawlerItem

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


class MySpider(Spider):
	name = "airbnb"
	allowed_domains = ['www.airbnb.com.ec']
	start_urls = generar_urls()

	def parse(self, response):

		rooms = Selector(response).xpath('//div[@class="col-sm-12 row-space-2 col-md-6"]')

		if rooms:
			
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
				yield request


	def parse_model(self, response):
		print 'dentro de la habitacion'

		inside_room = Selector(response).xpath('//div[@class="expandable-content expandable-content-long"]/div')

		reviews_count = Selector(response).xpath('//h4[@class="text-center-sm col-middle col-md-12"]')

		
		if inside_room:
			for room in inside_room:
				item = AirbnbWebcrawlerItem(response.meta["item"])

				if reviews_count:
					count_review = reviews_count.xpath('span/text()').extract()[0]
					item['data_review_count']=count_review

				descripcion = room.xpath('p')

				parrafo = []
				for p in descripcion:
					aux = p.xpath('span/text()').extract()[0]
					parrafo.append(aux)

				item['data_descripcion'] = ' '.join(parrafo)
				yield item











