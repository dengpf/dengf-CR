# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class OrangeItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    code = Field()  #  角色id
    position =Field()
    website = Field()
    webcode = Field()   #  网站的编码
    blog = Field()
    introduction = Field()

    addr = Field()
    role = Field()
    job = Field()
    education = Field()


    experience = Field()
