# __author__ = 'jimubox'
# coding:utf-8
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from person.items import OrangeItem


class OrangeSpider(Spider):
    name = 'Person'
    allowed_domains = [
        'itjuzi',
    ]
    start_urls = [
        'http://itjuzi.com/person',
    ]

    ## 在首页中取出总页数
    def parse(self, response):
        sel = Selector(response)
        amount = sel.xpath("//li[@class='next page']/a[@class = 'follow_link']/@href").extract()[1].rsplit('=', 1)[1]
        for pagenum in range(1, int(amount) + 1):
            url = "http://itjuzi.com/person?page=%s" % pagenum
            yield Request(url, callback=self.parse_item, dont_filter=True)

    ## 抓取每一页中生成请求24 个角色的信息
    def parse_item(self, response):
        sel = Selector(response)
        personurls = sel.xpath("//div[@class = 'media']/a/@href").extract()
        for personurl in personurls:
            yield Request(personurl, callback=self.parse_content, dont_filter=True)

    # 在详情页抓取信息
    def parse_content(self, response):
        orangeitem = OrangeItem()
        sel = Selector(response)

        orangeitem['code'] = response.url.rsplit('/', 1)[1]

        orangeitem['name'] = sel.xpath('//div[@class = "public-info pull-left"]/p/a/text()').extract()[0]

        content = sel.xpath("//section[@id='page-content']/article[@class='two-col-big-left']/div")
        try:
            orangeitem['webcode'] = content[0].xpath('div/div/ul/li/a/@href')[0].extract().rsplit('/', 1)[1]
        except:
            orangeitem['webcode'] = ''
        try:
            orangeitem['position'] = content[0].xpath('div/div/ul/li/a/text()')[0].extract() + \
                                     content[0].xpath('div/div/ul/li/text()')[1].extract()
        except:
            orangeitem['position'] = ''
        try:
            orangeitem['blog'] = content[0].xpath('div/div/ul/li[2]/a/text()').extract()[0]
        except:
            orangeitem['blog'] = ''
        try:
            orangeitem['introduction'] = content[0].xpath('div/div/ul/li[3]/em/text()').extract()[0]
        except:
            orangeitem['introduction'] = ''

        try:
            city = content[1].xpath('ul/li[1]/a/text()').extract()[0]
        except:
            city = ''
        try:
            district = content[1].xpath('ul/li[1]/em/text()').extract()[0]
        except:
            district = ''
        orangeitem['addr'] = city + district
        try:
            orangeitem['role'] = ','.join(content[1].xpath('ul/li[2]/a/text()').extract())
        except:
            orangeitem['role'] = ''
        try:
            orangeitem['job'] = content[1].xpath('ul/li[3]/a/text()').extract()[0]
        except:
            orangeitem['job'] = ''

        try:
            orangeitem['education'] = ','.join(content[1].xpath('ul/li[4]/a/text()').extract())
        except:
            orangeitem['education'] = ''

        orangeitem['experience'] = []
        try:
            exp = sel.xpath('//div[@id="company-similar"]/div')

            for i in exp:
                title = i.xpath('div/h4/text()').extract()[0].encode('utf8') + i.xpath('div/h4/a/text()').extract()[
                    0].encode('utf8') + i.xpath('div/h4/text()').extract()[1].encode('utf8')
                detail = i.xpath('div/p/text()').extract()[0]
                companyurl = i.xpath('div/h4/a/@href').extract()[0]
                orangeitem['experience'].append({'title': title, 'detail': detail, 'companyurl': companyurl})

        except:
            pass
        return orangeitem