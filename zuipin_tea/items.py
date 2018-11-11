# -*- coding: utf-8 -*-
import scrapy


class GoodsItem(scrapy.Item):
    title = scrapy.Field()
    detail = scrapy.Field()
    goods_title = scrapy.Field()
    goods_desc = scrapy.Field()
    scj_price = scrapy.Field()
    zp_price = scrapy.Field()
    brand = scrapy.Field()
    weight = scrapy.Field()
    goods_id = scrapy.Field()
    detail_desc = scrapy.Field()
    pl_id = scrapy.Field()
    url = scrapy.Field()
