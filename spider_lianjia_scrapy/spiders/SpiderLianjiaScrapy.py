#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2018/1/2 下午7:37
# @File : SpiderLianjiaScrapy.py
# @Software : IntelliJ IDEA
# @Email ： 909709223@qq.com
import json

import requests
import scrapy as scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class SpiderLianjiaScrapy(scrapy.Spider):
    name = "spider_lianjia_scrapy"
    start_urls = []
    # 读取城市配置
    with open('../city.json', 'r') as json_file:
        data = json.load(json_file)

    for i in data:
        # 上海苏州去掉
        if i['code'] != 'su' and i['code'] != 'sh':
            child_url = "https://%s.fang.lianjia.com/loupan/rs/"%i['code']
            r = requests.get(child_url)
            soup = BeautifulSoup(r.text, 'lxml', from_encoding='utf-8')
            count = soup.find(id='findCount').string
            # 整除判断
            page_count = 0
            if int(count) % 10 == 0:
                page_count = int(count)/10
            else:
                page_count = int(count)/10 + 1
            for x in range(page_count):
                start_urls.append("https://%s.fang.lianjia.com/loupan/pg%s"%(i['code'],x+1))
    for u in start_urls:
        print u

    def parse(self,response):
        url = response.url
        # TODO URL解析

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('spider_lianjia_scrapy')
    process.start()