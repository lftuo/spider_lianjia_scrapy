#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2018/1/2 下午7:37
# @File : SpiderLianjiaScrapy.py
# @Software : IntelliJ IDEA
# @Email ： 909709223@qq.com
import json
import logging

import requests
import scrapy as scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import urlparse
import urllib
import sys

from spider_lianjia_scrapy.items import SpiderLianjiaScrapyItem

reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderLianjiaScrapy(scrapy.Spider):
    name = "spider_lianjia_scrapy"
    start_urls = []
    # 读取城市配置
    with open('../city.json', 'r') as json_file:
        data = json.load(json_file)

    for i in data:
        # 上海苏州去掉
        if i['code'] != 'su' and i['code'] != 'sh':
            child_url = "https://%s.fang.lianjia.com/loupan/rs/%s"%(i['code'],i['city'])
            start_urls.append(child_url)

    def parse(self, response):
        url = response.url
        city_url = response.url[0:len(response.url)-18]
        city_name = urllib.unquote(url.split('/')[len(url.split('/')) - 1])
        item = SpiderLianjiaScrapyItem(city_name=city_name)
        request = scrapy.Request(url=city_url,callback=self.parse_detail)
        request.meta['item'] = item
        yield request

    def parse_detail(self, response):
        item = response.meta['item']
        city_name = item['city_name']
        # 按区解析URL
        url = response.url
        area_urls = response.xpath(".//*[@id='filter-options']/dl[@class='dl-lst clear']")[0].xpath("./dd[@class='dd show-more']/div[@class='option-list']/a")
        for area_url in area_urls:
            a_name = area_url.xpath("./text()").extract()[0]
            a_url = urlparse.urljoin(url,area_url.xpath("./@href").extract()[0])
            if a_name != '不限'.encode('utf-8'):
                item = SpiderLianjiaScrapyItem(city_name=city_name,a_name=a_name)
                request = scrapy.Request(url=a_url,callback=self.parse_house_pgs)
                request.meta['item'] = item
                yield request

    def parse_house_pgs(self, response):

        item = response.meta['item']

        # 计算总页数
        r = requests.get(response.url)
        soup = BeautifulSoup(r.text, 'lxml', from_encoding='utf-8')
        count = soup.find(id='findCount').string
        # 计算总页数，整除判断
        page_count = 0
        if int(count) % 10 == 0:
            page_count = int(count)/10
        else:
            page_count = int(count)/10 + 1

        # 存在房产数据时再进行解析
        if page_count > 0:
            for i in range(page_count):
                pg_url = response.url+'/pg%s'%(i+1)
                item = SpiderLianjiaScrapyItem(city_name=item['city_name'],a_name=item['a_name'])
                request = scrapy.Request(url=pg_url,callback=self.parse_hose_info)
                request.meta['item'] = item
                yield request

    def parse_hose_info(self, response):

        item = response.meta['item']

        # 遍历房产列表，获取小区信息
        house_lst = response.xpath(".//*[@id='house-lst']/li")
        for house in house_lst:
            try:
                house_info1 = house.xpath("./div[@class='info-panel']/div[@class='col-1']")
                house_name = house_info1.xpath("./h2/a/text()").extract()[0]
                house_url = urlparse.urljoin(response.url,house_info1.xpath("./h2/a/@href").extract()[0])
                house_where = house_info1.xpath("./div[@class='where']/span/text()").extract()[0]
                house_area = house_info1.xpath("normalize-space(./div[@class='area'])").extract()[0]
                house_other = house_info1.xpath("normalize-space(./div[@class='other'])").extract()[0]
                house_price = house.xpath("normalize-space(./div[@class='info-panel']/div[@class='col-2']/div[@class='price']/div[@class='average'])").extract()[0]

                print item['city_name'],item['a_name'],house_name,house_where,house_area,house_other,house_price,house_url
                item['house_name'] = house_name
                item['house_where'] = house_where
                item['house_area'] = house_area
                item['house_price'] = house_price
                item['house_url'] = house_url

                yield item
            except Exception,e:
                logging.exception(e)


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('spider_lianjia_scrapy')
    process.start()