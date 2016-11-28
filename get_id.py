# -*- coding: utf-8 -*-
# read article url, print wechatid
import sys
from lxml import etree
from wechatsogou.tools import *
from wechatsogou import *
import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger()
wechats = WechatSogouApi()

def get_id_from_url(urls = []):
    if len(urls) == 0: # no url is passed, read from stdin
        urls = sys.stdin
    for line in urls:
        this_url = line.strip()
        text = wechats._get(this_url, 'get', host='mp.weixin.qq.com')
        page = etree.HTML(text)
        wechatid = page.xpath('//p[@class="profile_meta"]/span/text()')[0]
        print wechatid

def get_urls_from_text(text):
    url = 'http://weixin.sogou.com/pcindex/pc/pc_0/pc_0.html'
    text = wechats._get(url)
    page = etree.HTML(text)
    return page.xpath('//li/div[2]/h3/a/@href')

def get_id_from_recent():
    kinds = range(19)
    page_iter = 0
    for kind in kinds:
        url = 'http://weixin.sogou.com/pcindex/pc/pc_' + str(kind) + '/pc_0.html'
        text = wechats._get(url)
        has_more = True
        miss_cnt = 0
        while has_more:
            page_iter += 1
            if '呀，出错啦！' in text:
                miss_cnt += 1
                if miss_cnt == 2:
                    has_more = False
            else:
                urls = get_urls_from_text(text)
                get_id_from_url(urls)
            page_idx = str(page_iter)
            url = 'http://weixin.sogou.com/pcindex/pc/pc_' + str(kind) + '/'+page_idx+'.html'
            text = wechats._get(url)

if __name__ == '__main__':
    get_id_from_recent()
