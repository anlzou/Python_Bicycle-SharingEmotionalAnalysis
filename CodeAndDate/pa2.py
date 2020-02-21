'''用于爬取指定页面的内容，把网页内容和图片分别保存为文件'''
import os
import urllib.request
import scrapy


class MySpider(scrapy.spiders.Spider):
    # 爬虫的名字，每个爬虫必须有不同的名字
    name = 'mySpider'
    allowed_domains = ['www.sdibt.edu.cn']
    # 要爬取的起始页面，必须是列表，可以包含多个url
    start_urls = ['http://www.sdibt.edu.cn/info/1026/11238.htm']

    # 对每个要爬取的页面，会自动调用下面这个方法
    def parse(self, response):
        self.downloadWebpage(response)
        self.downloadImages(response)

        # 检查页面中的超链接，并继续爬取
        hxs = scrapy.Selector(response)
        sites = hxs.xpath('//ul/li')
        for site in sites:
            link = site.xpath('a/@href').extract()[0]
            if link == '#':
                continue
            # 把相对地址转换成绝对地址
            elif link.startswith('..'):
                next_url = os.path.dirname(response.url)
                next_url += '/' + link
            else:
                next_url = link
            # 生成Request对象，并指定回调函数
            yield scrapy.Request(url=next_url, callback=self.parse_item)

    # 回调函数，对起始页面中的每个超链接起作用
    def parse_item(self, response):
        self.downloadWebpage(response)
        self.downloadImages(response)

    # 下载当前页面中所有的图片
    def downloadImages(self, response):
        hxs = scrapy.Selector(response)
        images = hxs.xpath('//img/@src').extract()
        for image_url in images:
            imageFilename = image_url.split('/')[-1]
            if os.path.exists(imageFilename):
                continue
            # 把相对地址转换成绝对地址
            if image_url.startswith('..'):
                image_url = os.path.dirname(response.url) + '/' + image_url
            # 打开网页图片
            fp = urllib.request.urlopen(image_url)
            # 创建本地图片文件
            with open(imageFilename, 'wb') as f:
                f.write(fp.read())
            fp.close()

    # 把网页内容保存为本地文件
    def downloadWebpage(self, response):
        filename = response.url.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)
