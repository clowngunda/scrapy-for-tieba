# -*- coding:utf-8 -*-

from scrapy import spider
import random
import requests
from scrapy.http import Request
from scrapy.selector import Selector                  #导入提取器
from scrscr.items import ScrscrItem                       #这里是导入了我们的item.py 里我们自己定义的类
import os




class scr(spider.Spider):                            #重写Spider
    name = "pic"                                    #唯一的爬虫名字
    #allowed_domains = ["blu-raydisc.tv"]              #允许的域，防止无限爬
    start_urls = [                                    #开始的urls
        "http://tieba.baidu.com/f?ie=utf-8&kw=%E7%81%B0%E5%8E%9F%E5%93%80&pn=0"]
    allowed_domains = ["tieba.baidu.com"]
    n=0
    num=0
    image_names={}




    def parse(self, response):                        #处理模块
        sel = Selector(response)                      #实例化Selector,参数为reponse
        item = ScrscrItem()                             #实例化我们自己定义item，可以理解为实例化字典
        #item['image_urls']=sel.xpath("//img[@class='BDE_Image']/@src").extract()
        #item['image_urls']=sel.xpath("//img/@src").extract()
        Links=sel.xpath('//*[@class="threadlist_title pull_left j_th_tit "]')
        #Links=sel.xpath('//*[@class="threadlist_title pull_left j_th_tit "]')
        for eachLink in Links:
            link_urls=eachLink.xpath('a/@href ').extract()
            #link_name=eachLink.xpath('a/@title ').extract()
            item['link_urls']=link_urls
            abc="".join(item['link_urls'])

            urld="http://tieba.baidu.com"+ abc+"?see_lz=1"
            responsed = requests.get(urld)
            responsed.encoding = 'gbk'
            item['image_urls']=Selector(responsed).xpath("//img[@class='BDE_Image']/@src").extract()
            for index,value in enumerate(item['image_urls']):
                self.num+=1
                self.image_names[value] = 'full/%d.jpg' % self.num
            yield item
        self.n+=50
        #连接基础url以及下页URl
        url="http://tieba.baidu.com/f?ie=utf-8&kw=%E7%81%B0%E5%8E%9F%E5%93%80&pn="
        if self.n<50000:
            url=url+str(self.n)
            yield Request(url,callback=self.parse)



