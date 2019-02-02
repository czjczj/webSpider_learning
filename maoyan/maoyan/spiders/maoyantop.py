# -*- coding: utf-8 -*-
import scrapy
from maoyan.items import MovieItem

class MaoyantopSpider(scrapy.Spider):
    name = "maoyantop"
    allowed_domains = ["maoyan.com"]
    start_urls = ['http://maoyan.com/']

    def parse(self, response):
        items = response.css('dl.board-wrapper dd')
        for dd in items:
            item = MovieItem()
            item['rank'] = dd.css('i.board-index::text').extract_first()
            item['imgUrl'] = dd.css('a img.board-img::attr(data-src)').extract_first()
            item['name'] = dd.css('a img.board-img::attr(alt)').extract_first()
            item['star'] = dd.css('div.board-item-main p.star::text').extract_first().strip().split("：")[1]
            item['releasetime'] = dd.css('div.board-item-main p.releasetime::text').extract_first().strip().split("：")[1]
            score_integer = dd.css('div.board-item-main i.integer::text').extract_first()
            score_fraction = dd.css('div.board-item-main i.fraction::text').extract_first()
            item['score'] = score_integer + score_fraction
            yield item
            

    def start_requests(self):
        baseUrl = "https://maoyan.com/board/4?offset="
        for i in range(0,self.settings.get('PAGE_NUM')):
            url = baseUrl + str(i*10)
            yield scrapy.Request(url,callback=self.parse)
