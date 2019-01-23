# -*- coding: utf-8 -*-
import copy
import scrapy
from youboy.items import YouboyItem

class YSpider(scrapy.Spider):
    name = 'y'
    # allowed_domains = ['youboy.com']
    # start_urls = ['http://youboy.com/']
    start_urls = ["http://www.youboy.com/"]
    base_url = 'http://www.youboy.com'
    # 这是一个动态域
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(YSpider, self).__init__(*args, **kwargs)
    # 获取所有大分类
    def parse(self,response):
        divs = response.xpath("//div[@class='col-xs-6']/div[@class='ui-index-classify-list']")
        for div in divs:
            for a in div.xpath("./ul/li/a"):
                item = YouboyItem()
                tag = a.xpath("./text()").extract_first()
                print(tag)
                item['tag'] = tag
                link = self.base_url + a.xpath("./@href").extract_first()
                yield scrapy.Request(link,callback=self.parse_page,meta={'item': item}, dont_filter=True)
    # 页面解析和翻页
    def parse_page(self, response):
        # print(response.url)
        item = response.meta['item']
        names = response.xpath("//div[@class='searchPdListConLItem']")
        for name in names:
            link=name.xpath(".//div[@class='pdListTitle']/p/a/@href").extract_first() + "contact.html"
            print(link)
            yield scrapy.Request(link,callback=self.parse_shop, meta={'item': item},dont_filter=True)
        next_page = response.xpath("//div[@class='searchPages']/span/a[@class='next']/@href")
        if next_page:
            yield scrapy.Request(next_page.extract_first(),callback=self.parse_page, meta={'item': item},dont_filter=True)
    # 详情也拿数据
    # 这里有几种网页格式，蛋疼，如果有更多那就全部写成函数放到一个文件里面
    def parse_shop(self,response):
        if response.text:
            item = response.meta['item']
            name = response.xpath("//div[@class='lianxi_wrap']/div[@class='lianxi']/p[1]/font/text()")
            if name:
                name= response.xpath("//div[@class='lianxi_wrap']/div[@class='lianxi']/p[1]/font/text()")
                name = name.extract_first() if len(name) >0 else None
                addr = response.xpath("//div[@class='lianxi_wrap']/div[@class='lianxi']/p[2]/i/text()")
                addr = ''.join(addr.extract()) if len(addr) >0 else None
                div = response.xpath("//div[@class='lianxi_wrap']/div[3]/ul")
                fa = div.xpath("./li[1]/text()")
                fa = ''.join(fa.extract()).strip('\n\t  ').strip('\r\n\t ') if len(fa) >0 else None
                tel1 = div.xpath("./li[2]/text()")
                tel1 = ''.join(tel1.extract()).strip('\r\n\t  ').strip('\t\r\n ') if len(tel1) >0 else None
                tel2 = div.xpath("./li[3]/text()")
                tel2 = ''.join(tel2.extract()).strip('\n\t  ').strip('\t\r\n\t ') if len(tel2) >0 else None
                email = div.xpath("./li[5]/text()")
                email = ''.join(email.extract()).strip('\n\t  ').strip('\r\n\t ') if len(email) >0 else None
                link = response.url
            elif response.xpath("//div[@class='contactCard']//tbody"):
                trs = response.xpath("//div[@class='contactCard']//tbody")[0]
                name = trs.xpath("./tr[1]/td[@class='nameTit01']/text()")
                name = name.extract_first() if len(name) else None
                addr = trs.xpath("./tr[2]/td/i/text()")
                addr = ''.join(addr.extract()) if len(addr) else None
                fa = trs.xpath("./tr[3]/td[2]/text()")
                fa = fa.extract_first() if len(fa) else None
                tel1 = trs.xpath("./tr[3]/td[4]/text()")
                tel1 = tel1.extract_first() if len(tel1) else None
                tel2 = trs.xpath("./tr[3]/td[6]/text()")
                tel2 = tel2.extract_first() if len(tel2) else None
                email = trs.xpath("./tr[4]/td[4]/text()")
                email = email.extract_first() if len(email) else None
                link = response.url
            elif response.xpath("//div[@class='lxcon']/ul"):
                div = response.xpath("//div[@class='lxcon']/ul")[0]
                name = div.xpath("./li[1]/b/font/text()")
                name = name.extract_first() if len(name) else None
                addr = div.xpath("./li[2]/i//text()")
                addr = ''.join(addr.extract()) if len(addr) else None
                fa = div.xpath("./li[3]/text()")
                fa = fa.extract() if len(fa) else None
                tel1 = div.xpath("./li[5]/text()")
                tel1 = tel1.extract() if len(tel1) else None
                tel2 = div.xpath("./li[6]/text()")
                tel2 = tel2.extract() if len(tel2) else None
                email = div.xpath("./li[9]/a/text()")
                email = email.extract() if len(email) else None
                link = response.url
            elif response.xpath("//tbody/tr/td[1]/strong/text()"):
                name = response.xpath("//tbody/tr/td[1]/strong/text()")
                name = name.extract_first() if len(name) else None
                addr = response.xpath("//tbody/tr/td[1]/p/text()[1]")
                addr = ''.join(addr.extract()) if len(addr) else None
                fa = response.xpath("//tbody/tr/td[1]/p/text()[3]")
                fa = fa.extract_first() if len(fa) else None
                tel1 = response.xpath("//tbody/tr/td[1]/p/text()[4]")
                tel1 = tel1.extract_first() if len(tel1) else None
                tel2 = response.xpath("//tbody/tr/td[1]/p/text()[5]")
                tel2 = tel2.extract_first() if len(tel2) else None
                email = response.xpath("//tbody/tr/td[1]/p/text()[7]")
                email = email.extract_first() if len(email) else None
                link = response.url
            else:
                div = response.xpath("//div[@class='contactCard']/div/ul")[0]
                name = div.xpath("./li[1]/strong/text()")
                name = name.extract_first() if len(name) > 0 else None
                addr = div.xpath("./li[2]/span//text()")
                addr = ''.join(addr) if len(addr) > 0 else None
                fa = div.xpath("./li[3]/span/text()")
                fa = fa.extract_first() if len(fa) > 0 else None
                tel1 = div.xpath("./li[4]/span/text()")
                tel1 = tel1.extract_first() if len(tel1) > 0 else None
                tel2 = div.xpath("./li[5]/span/text()")
                tel2 = tel1.extract_first() if len(tel2) > 0 else None
                email = div.xpath("./li[7]/span/text()")
                email = email.extract_first() if len(email) > 0 else None
                link = response.url

            item['name'] = name
            item['addr'] = addr
            item['fa'] = fa
            item['tel1'] = tel1
            item['tel2'] = tel2
            item['email'] = email
            item['link'] = link
            print(item)
            yield item




