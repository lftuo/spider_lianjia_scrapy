# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import time
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi


class SpiderLianjiaScrapyPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    # pipeline默认调用
    def process_item(self, item,spider):
        # 此处可进行数据清洗ETL
        item = self.data_etl(item)
        self.dbpool.runInteraction(self.__conditional_insert,item)
        return item

    def data_etl(self,item):
        price = item['house_price'].replace('均价 ','')
        if ' 元/平' in price:
            price.replace(' 元/平','')
        # TODO 万/套的数据清洗
        item['house_price'] = price
        return item

    def __conditional_insert(self, tx, item):
        spider_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = "insert into spider_lianjia_new_house(city_name,area_name,house_name,house_where,house_area,house_price,house_url,spider_time) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            params = (item['city_name'],item['a_name'],item['house_name'],item['house_where'],item['house_area'],item['house_price'],item['house_url'],spider_time)
            tx.execute(sql, params)
        except Exception, e:
            logging.exception(e)

    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)


