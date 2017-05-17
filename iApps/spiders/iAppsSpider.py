# -*- coding: utf-8 -*-
import scrapy


class IappsspiderSpider(scrapy.Spider):
    name = "iAppsSpider"
    # allowed_domains = ["http://www.iapps.im/single/"]
    start_urls = ['http://www.iapps.im/single/',]
    # 定义一个终止爬虫的url，爬到该url时爬虫自动停止
    stop_url = 'http://www.iapps.im/lists/0/page/11'

    def parse(self, response):
        items = response.css('#list-wrap')
        for item in items:
            yield {
                'item_title': " ".join(item.css('h2>a>span::text').extract()),
                'item_desc': item.css("div.entry-content>p::text").extract(),
                'item_meta': item.css("div.entry-meta.clearfix>div.pull-left>a::text").extract(),
                'item_hot': item.css(
                    "div.entry-meta.clearfix>div.pull-right>a::text").extract()[0].strip(),
                'item_commit': item.css(
                    "div.entry-meta.clearfix>div.pull-right>a::text").extract()[2].split()[0],
                'item_recommand_time': " ".join(item.css(
                    "div.entry-meta.clearfix>div.pull-left::text").extract()[-1].split()),
            }
        # first_page = response.xpath(
        #     '//*[(@id = "content")]//li[(((count(preceding-sibling::*) + 1) = 9) and parent::*)]//a/@href').extract_first()
        # other_page = response.xpath(
        #     '//*[(@id = "content")]//li[(((count(preceding-sibling::*) + 1) = 10) and parent::*)]//a/@href').extract_first()
        next_page = response.xpath(
            '//*[@id="content"]/div[2]/ul/li')[-2].xpath('a/@href').extract_first()
        if next_page == IappsspiderSpider.stop_url:
            next_page = None
        # yield {
        #     'next_page': next_page,
        #     }
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
