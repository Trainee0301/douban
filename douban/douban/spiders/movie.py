# -*- coding: utf-8 -*-
import scrapy

from douban.items import DoubanItem


class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_list = response.xpath('//div[@class="article"]//ol[@class="grid_view"]/li')
        for i in movie_list:
            douban_item = DoubanItem()
            douban_item['movie_top'] = i.xpath('.//div[@class="item"]/div[@class="pic"]//em/text()').extract_first()
            douban_item['movie_name'] = i.xpath('.//div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/span[1]/text()').extract_first()
            contents = i.xpath('.//div[@class="item"]/div[@class="info"]//div[@class="bd"]/p[1]/text()').extract()
            for content in contents:
                content_s = "".join(content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i.xpath('.//span[@class="rating_num"]/text()').extract_first()
            douban_item['evaluate'] = i.xpath('.//div[@class="star"]//span[4]/text()').extract_first()
            douban_item['describe'] = i.xpath('.//p[@class="quote"]/span/text()').extract_first()
            yield douban_item
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        # next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
