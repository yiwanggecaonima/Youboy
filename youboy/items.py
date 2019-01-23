# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class YouboyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    addr = Field()
    tel1 = Field()
    tel2 = Field()
    email = Field()
    link = Field()
    fa= Field()

