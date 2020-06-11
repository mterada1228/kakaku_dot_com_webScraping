#!/bin/bash

<< COMMENTOUT
  価格.com の spider を実行する
COMMENTOUT

cd $(dirname $0)

. /home/ubuntu/dev/webScraping/scraping/bin/activate

scrapy crawl kakaku_dot_com
