#!/bin/sh
scrapy runspider tsum_spider.py -o tsum_items.json -t jsonlines -L INFO
