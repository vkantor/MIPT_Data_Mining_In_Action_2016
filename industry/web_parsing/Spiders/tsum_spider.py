# -*- encoding: utf8 -*-

import scrapy
import requests
import pandas

def get_url_id(url):
    return url.split("/")[-1].split(".html")[0]

class TsumSpider(scrapy.Spider):
    name = "tsum"   
    def __init__(self, domain='http://www.tsum.ru'):
        self.domain = domain
        urls_df = pandas.read_pickle('tsum_item_urls.pickle')
        self.urls = list(urls_df["item_url_path"])
    
    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(self.domain + url)
            
    def parse(self, response):
        params_dict = dict(zip(response.css("div.b-options-list__header ::text").extract(), response.css("div.b-options-list__desc ::text").extract()))
        record = {
            "url": response.url,
            "url_id": get_url_id(response.url),
            "vendor": response.css("h1.b-goods-inner__name > span > strong > a ::text").extract_first(),
            "name": response.css("h1.b-goods-inner__name > span ::text").extract()[1],
            "price": int(response.css("span.b-goods-inner__price-size ::text").extract_first().replace(" ", "")),
            "sizes": "\t".join(response.css("span.b-goods-inner__size-num ::text").extract()),
            "consist": params_dict.get(u"Состав", u""),
            "country": params_dict.get(u"Страна производства", u""),
            "tech_description": params_dict.get(u"Техническое описание", u""),
            "categories": "\t".join(response.css("a.b-breadcrumbs__link.hidden-lg ::text").extract()),
            "colors": "\t".join(response.css("div.b-goods-inner__colors").css("div.b-goods-gallery__small-img ::attr(title)").extract()),
            "discont_price": int(response.css("div.b-goods-inner__colors")[0].css("div.b-goods-gallery__small-img")[0].css("::attr(data-discontprice)").extract_first().replace(" ", ""))
        }
        
        record["sales_id"] = int(response.css("div.b-goods-inner__colors")[0].css("div.b-goods-gallery__small-img")[0].css("::attr(data-product)").extract_first())
        
        yield record
        
