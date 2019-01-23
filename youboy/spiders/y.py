# -*- coding: utf-8 -*-
import scrapy
from youboy.items import YouboyItem

class YSpider(scrapy.Spider):
    name = 'y'
    # allowed_domains = ['youboy.com']
    # start_urls = ['http://youboy.com/']
    start_urls = ["http://www.youboy.com/p/_74957.html"]
    base_url = 'http://www.youboy.com'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(YSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # print(response.url)
        names = response.xpath("//div[@class='searchPdListConLItem']")
        for name in names:
            link=name.xpath(".//div[@class='pdListTitle']/p/a/@href").extract_first() + "contact.html"
            print(link)
            yield scrapy.Request(link,callback=self.parse_shop,dont_filter=True)
        next_page = response.xpath("//div[@class='searchPages']/span/a[@class='next']/@href")
        if next_page:
            yield scrapy.Request(next_page.extract_first(),callback=self.parse,dont_filter=True)

    def parse_shop(self,response):
        if response.text:
            item = YouboyItem()
            name = response.xpath("//div[@class='lianxi_wrap']/div[@class='lianxi']/p[1]/font/text()")
            if name:
                name= response.xpath("//div[@class='lianxi_wrap']/div[@class='lianxi']/p[1]/font/text()").extract_first()
                addr = response.xpath("//div[@class='lianxi_wrap']/div[@class='lianxi']/p[2]/i/text()").extract_first()
                div = response.xpath("//div[@class='lianxi_wrap']/div[3]/ul")
                fa = ''.join(div.xpath("./li[1]/text()").extract()).strip('\n\t  ').strip('\r\n\t ')
                tel1 = ''.join(div.xpath("./li[2]/text()").extract()).strip('\r\n\t  ').strip('\t\r\n ')
                tel2 = ''.join(div.xpath("./li[3]/text()").extract()).strip('\n\t  ').strip('\t\r\n\t ')
                email = ''.join(div.xpath("./li[5]/text()").extract()).strip('\n\t  ').strip('\r\n\t ')
                link = response.url
            elif response.xpath("//div[@class='contactCard']//tbody"):
                trs = response.xpath("//div[@class='contactCard']//tbody")
                name = trs.xpath("./tr[1]/td[@class='nameTit01']/text()").extract_first()
                addr = trs.xpath("./tr[2]/td/i/text()").extract_first()
                fa = trs.xpath("./tr[3]/td[2]/text()").extract_first()
                tel1 = trs.xpath("./tr[3]/td[4]/text()").extract_first()
                tel2 = trs.xpath("./tr[3]/td[6]/text()").extract_first()
                email = trs.xpath("./tr[4]/td[4]/text()").extract_first()
                link = response.url
            elif response.xpath("//div[@class='lxcon']/ul"):
                div = response.xpath("//div[@class='lxcon']/ul").extract_first()
                name = div.xpath("./li[1]/b/font/text()").extract_first()
                addr = div.xpath("./li[2]/i//text()").extract_first()
                fa = div.xpath("./li[3]/text()").extract()
                tel1 = div.xpath("./li[5]/text()").extract()
                tel2 = div.xpath("./li[6]/text()").extract()
                email = div.xpath("./li[9]/a/text()").extract()
                link = response.url
            else:
                name = response.xpath("//tbody/tr/td[1]/strong/text()").extract_first()
                addr = response.xpath("//tbody/tr/td[1]/p/text()[1]").extract_first()
                fa = response.xpath("//tbody/tr/td[1]/p/text()[3]").extract_first()
                tel1 = response.xpath("//tbody/tr/td[1]/p/text()[4]").extract_first()
                tel2 = response.xpath("//tbody/tr/td[1]/p/text()[5]").extract_first()
                email = response.xpath("//tbody/tr/td[1]/p/text()[7]").extract_first()
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




