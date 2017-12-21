# -*- coding: cp936
from functools import partial
import scrapy

class HupuGearSpider(scrapy.Spider):
    name = 'hupu gear spider'
    start_urls = ['http://bbs.hupu.com/gear-{page}'.format(page=page) for page in range(1, 101) ]
    
    def parse(self, response):
        for message in response.css('table#pl tbody tr'):
            mid = message.css('::attr(mid)').extract()[0]
            url = response.urljoin('./{mid}.html'.format(mid=mid))
            yield scrapy.Request(url, callback = partial(self.parse_message, mid))

    def parse_message(self, mid, response):
        fid = 0
        for floor in response.css('div.floor'):
            uid = floor.css('div.user div.j_u::attr(uid)').extract()[0]
            stime = floor.css('div.floor_box div.author div.left span.stime::text').extract()[0]
            content = u'，'.join(map(lambda x:x.strip(), floor.css('div.floor_box table.case tr td::text').extract()))
            if fid == 0:
                title = floor.css('div.floor_box table.case tr td div.subhead span::text').extract()[0]
                content = title + u'。' + content
            ret = {'mid':mid, 'fid':fid, 'uid':uid, 'stime':stime, 'content':content}
            fid += 1
            yield ret
