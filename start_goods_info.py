# -*- coding:utf-8 -*-
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl goods_info -o goods_info.csv -s JOBDIR=job_info/goods_info".split())
