# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo


class YouboyPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('./youboy_items.json', 'a',encoding='utf-8')

    def process_item(self, item, spider):
        if item['name']:
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
        return item

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_port,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.i = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'), mongo_port=crawler.settings.get('MONGO_PORT'),mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("", 27017,connect=True)
        self.db = self.client['scrapy_hc']

    def process_item(self,item,spider):
        # if isinstance(item,HcItemItem):
        collection = 'Youboy'
        # if self.db[collection].update({'name': item['name']}, {'$set': dict(item)}, True):
        if item['name']:
            # if self.db[collection].update({'name':item['name']},{'$set': dict(item)},True):
            if self.db[collection].insert(dict(item)):
                print('Sueecss saved to Mongodb',item['name'])
                self.i +=1
                print(self.i)
            else:
                print('Not Mongodb ')

        return item
