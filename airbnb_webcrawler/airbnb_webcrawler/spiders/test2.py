from scrapy import Spider
from scrapy.selector import Selector
from airbnb_webcrawler.items import AirbnbWebcrawlerItem

class MySpider2(Spider):
	name = "airbnb2"
	allowed_domains = ['https://www.airbnb.com.ec/']
	start_urls = ['https://www.airbnb.com.ec/s/London--United-Kingdom?ss_id=vgev4c7y']

	def parse(self, response):
		sites = hxs.select('//div[@class="col-sm-12 row-space-2 col-md-6"]')
		items = []

		request = Request("https://www.airbnb.com.ec/s/London--United-Kingdom?ss_id=vgev4c7y", callback=self.parseDescription1)
		request.meta['item'] = item
		yield request

		yield Request("http://www.example.com/lin1.cpp", callback=self.parseDescription2, meta={'item': item})


	def parseDescription1(self,response):
		print xpath('div[@class="listing"]/@data-url').extract()[0]
		return xpath('div[@class="listing"]/@data-url').extract()[0]

	def parseDescription2(self,response):
		print xpath('//div[@class="expandable-content expandable-content-long"]/divp/p/span/')
		return xpath('//div[@class="expandable-content expandable-content-long"]/divp/p/span/')