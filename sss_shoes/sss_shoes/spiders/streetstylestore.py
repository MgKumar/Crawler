# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sss_shoes.items import SssShoesItem
from scrapy.http.request import Request

class StreetstylestoreSpider(scrapy.Spider):
    name = 'streetstylestore'
    allowed_domains = ['www.streetstylestore.com']
    start_urls = ['http://streetstylestore.com/index.php?id_cms=50&controller=cms']
  
    def parse(self, response):
       link= response.xpath('//div[@class="new-cat-sub-cat"]/ul/li//a/@href').extract()
       for l in link:
           yield scrapy.Request(l,callback = self.parse_url,dont_filter=True)

    def parse_url(self, response):
       url = response.xpath('//div[@class="prd"]//div[@class="item-info"]/a[@class="product-name"]/@href').extract()
       for link in url:
           yield scrapy.Request(link,callback = self.parse_item,dont_filter=True)
           
    def parse_item(self,response):
          
           item = SssShoesItem()
           item['url'] = response.url
           item['product_name'] = response.xpath('//div[@class="product_desc"]//p//strong/text()').extract_first()
           item['product_price'] = response.xpath('//div[@class="price"]/p/span[@id="our_price_display"]/text()').extract_first()
           yield item
    


    
