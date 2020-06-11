import scrapy
import re
from kakaku_dot_com.items import KakakuDotComItem
import os
import requests

class KakakuDotComSpider(scrapy.Spider):

    name = 'kakaku_dot_com'
    allowed_domains = ['kakaku.com']
    start_urls = ['https://kakaku.com/item/J0000031201/']

    SLACK_INCOMING_WEBHOOK_URL = 'https://hooks.slack.com/services/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'

    def parse(self, response):

        """ start_urlに指定した商品の最安値を取得する。  """

        item = KakakuDotComItem('')

        item['product_id'] = re.search(r'item\/(\w+)', response.url).group(1)
        item['product_name'] = response.css('div.itmTitleArea > #titleBox > .boxL').xpath('string()').get().strip()
        item['cheapest_value'] = re.search(r'\¥(\S*)', response.css('div.subInfoObj1 > p > span').xpath('string()').get()).group(1).replace(',', '')

        # 価格が32,000以下であればslackに通知する
        threthold = 32000
        if int(item['cheapest_value']) <= threthold:
            requests.post(self.SLACK_INCOMING_WEBHOOK_URL, json={'text': f'{self.start_urls[0]} \n 値段が{threthold}円以下になりました!'})      

        yield item
