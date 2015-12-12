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

    
class AirbnbUKItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    latitud = Field()
    longitud = Field()
    nombre = Field()
    ubicacion = Field()
    costo = Field()
    acomodados = Field()
    banios = Field()
    cama_tipo = Field()
    cuartos = Field()
    camas = Field()
    check_in = Field()
    check_out = Field()
    tipo_propiedad = Field()
    tipo_habitacion = Field()
    servicios = Field()
    descripcion = Field()
    reglas = Field()
    reviews = Field()
