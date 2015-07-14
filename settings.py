# -*- coding: utf-8 -*-

BOT_NAME = 'person'

SPIDER_MODULES = ['person.spiders']
NEWSPIDER_MODULE = 'person.spiders'


ITEM_PIPELINES = {
    'pipelines.OrangePipeline':100,
}

