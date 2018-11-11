# -*- coding: utf-8 -*-
import re
import scrapy
from zuipin_tea.items import GoodsItem


class GoodsInfoSpider(scrapy.Spider):
    name = 'goods_info'
    allowed_domains = ['zuipin.cn']
    # start_urls = ['https://www.zuipin.cn/goods?id=ZONGY0840-250']
    start_urls = ['https://www.zuipin.cn/']

    def parse(self, response):
        big_title_list = response.xpath("//dl[@class='clearfix']")
        for big_title in big_title_list:
            title = big_title.xpath("./dt[@class='big-title float-left']/a/text()").extract_first()
            small_list = big_title.xpath(".//li/a[2]")
            for small in small_list:
                detail = small.xpath("./text()").re_first(r"[\u4e00-\u9fa5]+")
                part_url = small.xpath("./@href").extract_first()
                url = response.urljoin(part_url)

                yield scrapy.Request(url=url,
                                     callback=self.second_parse,
                                     meta={'title': title, 'detail': detail, 'page': 1, 'base_url': url})

    def second_parse(self, response):
        total_page = response.xpath("//span[@class='endClass']/text()").re_first('\d')
        title, detail = response.meta['title'], response.meta['detail']
        page, base_url = response.meta['page'], response.meta['base_url']

        # 为了避免 获取到一个异常的 页码
        if total_page:
            next_page = page + 1
            if next_page <= int(total_page):
                url = base_url + '&page={}'.format(next_page)
                yield scrapy.Request(url=url,
                                     callback=self.second_parse,
                                     meta={'title': title, 'detail': detail, 'page': next_page, 'base_url': url})
            else:
                self.logger.info(f'总页数{total_page} url={response.url}')
        else:
            self.logger.error(f'没有页数了??? url={response.url}')

        info_url_list = response.xpath("//div[@class='item float-left']//a/@href").extract()
        for part_info_url in info_url_list:
            info_url = response.urljoin(part_info_url)
            yield scrapy.Request(url=info_url,
                                 callback=self.info_parse,
                                 meta={'title': title, 'detail': detail})

    def info_parse(self, response):
        # def parse(self, response):
        item = GoodsItem()
        url = response.url
        title, detail = response.meta['title'], response.meta['detail']
        goods_title = response.xpath("//h1[@class='g-title']/text()").extract_first()
        goods_desc = response.xpath("//p[@class='g-scr']/text()").extract_first()
        scj_price0 = response.xpath("//del[@class='scj']/text()").re_first("\S+")
        scj_price = f"{scj_price0}元"
        zp_price0 = response.xpath("//span[@class='zp  hy ']/text()").re_first("\S+")
        zp_price = f"{zp_price0}元"
        brand = response.xpath("//ul[@class='clearfix']/li[1]/span[@class='g-con']/text()").extract_first()
        weight = response.xpath("//ul[@class='clearfix']/li[2]/span[@class='g-con']/text()").extract_first()
        goods_id = response.xpath("//ul[@class='clearfix']/li[3]/span[@class='g-con']/text()").extract_first()
        xqms = response.xpath("//dt/ul[@class='clearfix']/li")  # 详细描述
        detail_desc = [''.join(i.xpath('string(.)').re("\S+")) for i in xqms]
        ret = re.search(r"var proExtId    = '(\d+)';", response.text)
        pl_id = ret.group(1) if ret else ret  # 评论id
        for field in item.fields:
            item[field] = eval(field)
        yield item
