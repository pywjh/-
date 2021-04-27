#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-06-23 12:00:38
# Project: wall

import os
from pyspider.libs.base_handler import *
from urllib import request


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://pic.netbian.com/', callback=self.page)
        
        
    @config(age=10 * 24 * 60 * 60)
    def page(self, response):
        for i in range(1, 100):
            self.crawl('http://pic.netbian.com/index_%d.html'%i, callback=self.detail_img)
            
    @config(priority=2)
    def detail_img(self, response):
        for each in response.doc('li > a').items():
            if '/tupian/' in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        for each in response.doc('#img > img').items():
            # print(each.attr.src)
            # print(each.attr.title)
            base_dir = 'D:/PRIVATE/scrapy_wallparper/wallparper'
            list_dir = os.listdir(base_dir)
            wall_name = each.attr.title + '.jpg'
            wall_path = base_dir + '/' + wall_name
            # print(wall_path)
            if wall_name not in list_dir:
                request.urlretrieve(
                    each.attr.src,
                    wall_path
                )
