# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KakakuDotComItem(scrapy.Item):
    
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    cheapest_value = scrapy.Field()

    def __unicode__(self):
        return repr(self).decode('unicode_escape')