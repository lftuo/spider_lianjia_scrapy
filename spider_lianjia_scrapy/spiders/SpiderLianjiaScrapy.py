#!/usr/bin/python
# -*- coding:utf8 -*-
# @Author : tuolifeng
# @Time : 2018/1/2 下午7:37
# @File : SpiderLianjiaScrapy.py
# @Software : IntelliJ IDEA
# @Email ： 909709223@qq.com
import scrapy as scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SpiderLianjiaScrapy(scrapy.Spider):
    name = "spider_lianjia_scrapy"
    start_urls = []
    # 读取城市配置
    for i in (100):
        start_urls.append(i)

    def parse(self,response):
        text = response.xpath('')


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('spider_lianjia_scrapy')
    process.start()