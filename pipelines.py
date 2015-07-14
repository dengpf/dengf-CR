# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
from datetime import datetime
from shutil import move as os_move
from shutil import rmtree
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class OrangePipeline(object):
    count = 0
    filecount = 0
    limit = 1000

    def open_spider(self, spider):
        self.f = open('itemout_' + str(self.filecount) + '.json', 'a+')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        self.count = self.count + 1
        if(self.count > self.limit):
            self.filecount = self.filecount + 1
            self.f = open('itemout_' + str(self.filecount) + '.json', 'a+')
            self.count = 1
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.f.write(line)
        return item
