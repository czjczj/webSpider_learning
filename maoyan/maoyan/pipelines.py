# -*- coding: utf-8 -*-
import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline
class MaoYanMoviePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['imgUrl'])

    def item_completed(self, results, item, info):
        img_path = [x['path'] for ok, x in results if ok]
        print(img_path)
        if not img_path:
            raise scrapy.exceptions.DropItem("DropItem error")
        item['saveUrl'] = img_path
#        print(item['saveUrl'])
        return item
    
    #https://p0.meituan.net/movie/093d9f90022cc283189288535d4cdc353508848.jpg@160w_220h_1e_1c
    def file_path(self, request, response=None, info=None):
        file_path = request.url.split('/')[-1].split('@')[0]
        return file_path
    
    
class MySqlMaoYan(object):
    def __init__(self, host, user, pwd, database, table):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.database = database
        self.table = table
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
             host = crawler.settings.get('MYSQL_HOST'),
             user= crawler.settings.get('MYSQL_USER'),
             pwd = crawler.settings.get('MYSQL_PWD'),
             database = crawler.settings.get('MYSQL_DATABASE'),
             table = crawler.settings.get('MYSQL_TABLE')
        )
        
    def open_spider(self,spider):
        self.db = pymysql.connect(self.host, self.user, self.pwd, self.database)
        self.cursor = self.db.cursor()
        print(self.db)
        print(self.cursor)
        
        """
        rank = scrapy.Field()
        name = scrapy.Field()
        star = scrapy.Field()
        releasetime = scrapy.Field()
        score = scrapy.Field()
        imgUrl = scrapy.Field()
        saveUrl = scrapy.Field()
        """
    def process_item(self, item, spider):
        sql = "insert into "+self.table+"(rank,name,star,releasetime,score,imgUrl,saveUrl) values(%s,%s,%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql,(item['rank'],
                                     item['name'],
                                     item['star'],
                                     item['releasetime'],
                                     item['score'],
                                     item['imgUrl'],
                                     item['saveUrl']
                                     ))
            self.db.commit()
        except:
            print("Insert Error:" + (item['saveUrl'] == None))
            self.db.rollback()
            
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()
        
        
class MaoyanPipeline(object):
    def process_item(self, item, spider):
        return item
