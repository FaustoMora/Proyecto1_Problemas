# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AirbnbWebcrawlerItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    data_id = Field()
    data_name = Field()
    data_user = Field()
    data_lat = Field()
    data_lng = Field()
    data_url = Field()
    data_descripcion = Field()

    
