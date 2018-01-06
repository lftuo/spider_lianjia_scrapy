# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderLianjiaScrapyItem(scrapy.Item):
    # define the fields for your item here like:

    # 城市名称
    city_name = scrapy.Field()
    # 区域名称
    a_name = scrapy.Field()
    # 房子名称
    house_name = scrapy.Field()
    # 房子所在地
    house_where = scrapy.Field()
    # 房子大小/面积等
    house_area = scrapy.Field()
    # 房子价格
    house_price = scrapy.Field()
    # 房产链接
    house_url = scrapy.Field()
