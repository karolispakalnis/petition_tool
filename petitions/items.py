# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PetitionsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    petition_id = scrapy.Field()
    timestamp = scrapy.Field()
    snapshot_url = scrapy.Field()
    signature_count = scrapy.Field()

    pass
