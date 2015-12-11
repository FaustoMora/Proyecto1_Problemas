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
    data_review_count = Field()

    
class AirbnbUKItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    latitud = scrapy.Field()
    longitud = scrapy.Field()
    nombre = scrapy.Field()
    ubicacion = scrapy.Field()
    costo = scrapy.Field()
    acomodados = scrapy.Field()
    banios = scrapy.Field()
    cama_tipo = scrapy.Field()
    cuartos = scrapy.Field()
    camas = scrapy.Field()
    check_in = scrapy.Field()
    check_out = scrapy.Field()
    tipo_propiedad = scrapy.Field()
    tipo_habitacion = scrapy.Field()
    servicios = scrapy.Field()
    descripcion = scrapy.Field()
    reglas = scrapy.Field()
    reviews = scrapy.Field()
    pass
