# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pdb
import MySQLdb

class KakakuDotComPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLPipeline:

    """ item を MySQLに保存するPipeline """

    def open_spider(self, spider):

        """ MySQL に接続。
            テーブルがないとくは作成する。 """

        settings = spider.settings

        params = {
            'host': settings.get('MYSQL_HOST', 'localhost'),
            'db': settings.get('MYSQL_DATABASE', 'scraping'),
            'user': settings.get('MYSQL_USER', ''),
            'passwd': settings.get('MYSQL_PASSWORD', ''),
            'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
        }

        self.conn = MySQLdb.connect(**params)        
        self.c = self.conn.cursor()

        # テーブルが存在しなければ作成する
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS `kakaku_dot_com_items` (\
                `id` INTEGER NOT NULL AUTO_INCREMENT, \
                `product_id` VARCHAR(200) NOT NULL, \
                `product_name` VARCHAR(200) NOT NULL, \
                `cheapest_value` INTEGER NOT NULL, \
                `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, \
                PRIMARY KEY(`id`)
                )
        """)

        self .conn.commit()

    def close_spider(self, spider):

        """ Spider の終了で MySQLサーバへの接続を切断する """

        self.conn.close()

    def process_item(self, item, spider):

        """ kakaku_dot_com_items デーブルに item を格納する """

        self.c.execute('INSERT INTO `kakaku_dot_com_items` (`product_id`, `product_name`,`cheapest_value`) \
                        VALUES (%(product_id)s, %(product_name)s, %(cheapest_value)s)', dict(item))
        self.conn.commit()

        return item