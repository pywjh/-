import os
import sys
import time
import argparse
import random
import requests
import difflib
from lxml import etree
from urllib.request import urlretrieve


class WallParper():

    category_dict = {
        '热度': '',
        '风景': '4kfengjing',
        '美女': '4kmeinv',
        '游戏': '4kyouxi',
        '动漫': '4kdongman',
        '影视': '4kyingshi',
        '明星': '4kmingxing',
        '汽车': '4kqiche',
        '动物': '4kdongwu',
        '人物': '4krenwu',
        '美食': '4kmeishi',
        '宗教': '4kzongjiao',
        '背景': '4kbeijing',
    }

    def __init__(self, all_page, category):
        super().__init__()
        self.worklist = []
        self.all_page = all_page
        self.url_value = self.category_dict.get(category, '')
        self.url = 'http://pic.netbian.com/{}'.format(self.url_value)
        self.base_url = 'http://pic.netbian.com'
        self.session = requests.session()
        self.session.encoding = 'utf-8'
        self.session.get(self.url)
        self.page = 2
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        self.session.headers.update(self.headers)

    def response(self, html):
        return etree.HTML(html)

    def search_img(self):
        all_page = self.all_page + 1
        for page in range(1, all_page):
            if page == 1:
                url = self.url
            else:
                url = f"{self.url}/index_{page}.html"
            html = self.response(self.session.get(url).text)
            for url in html.xpath('//ul[@class="clearfix"]/li/a/@href'):
                self.worklist.append(f"{self.base_url}{url}")

    def download(self, src, img_name, download_img_name):
        try:
            urlretrieve(
                url=f"{self.base_url}{src}",
                filename=img_name
            )
            print(f"{download_img_name} - 下载成功！")
        except Exception as e:
            print(f"{download_img_name} - 下载失败！::: {str(e)}")

    def download_img(self):
        dir_name = f"wallparper_{self.url_value or 'redu'}".replace("4k", '')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        for url in self.worklist:
            try:
                response = requests.get(url, headers=self.headers, timeout=2)
            except requests.Timeout:
                print(url, '请求超时，已经跳过')
                response = False
            if response:
                response.encoding = 'GBK'
                html = self.response(response.text)
                src = html.xpath('//a[@id="img"]/img/@src')[0]
                title = html.xpath('//a[@id="img"]/img/@title')[0]
                
                download_img_name = f"{title}.jpg"
                img_name = f"{dir_name}/{title}.jpg"

                if os.listdir(dir_name):
                    if download_img_name not in os.listdir(dir_name):
                        like_ratio = max(map(lambda l: difflib.SequenceMatcher(None, download_img_name, l).quick_ratio(), os.listdir(dir_name)))
                        if like_ratio > 0.9:  # 标题相似度大于0.9的也不下载
                            print(f"{download_img_name} - 已存在，跳过下载")
                        else:
                            self.download(src, img_name, download_img_name)
                    else:
                        print(f"{download_img_name} - 已存在，跳过下载")
                else:
                    self.download(src, img_name, download_img_name)
                

            time.sleep(round(random.random(), 2))

    def __call__(self):
        print('请注意，你当前的壁纸会下载到此路径：', os.getcwd())
        self.search_img()
        self.download_img()


if __name__ == "__main__":
    
    #
    # parser = argparse.ArgumentParser(description='传入一个数字代表爬取的页数和类型，一页21张图片')
    # #type是要传入的参数的数据类型  help是该参数的提示信息
    # parser.add_argument('-p', type=str, help='页数')
    # parser.add_argument(
    #     '-c',
    #     type=str,
    #     help='类型: 热度、风景、美女、游戏、动漫、影视、明星、汽车、动物、人物、美食、宗教、背景',
    #     default='热度',
    #     )

    # args = parser.parse_args()
    #
    # page = args.p
    # category = args.c
    #
    # try:
    #     page = int(page)
    # except TypeError:
    #     print('页数传入有误')

    # print(page, category)
    category = str(input("请輸入你想下载的类型：（重复的不会下载）\n'热度'、'风景'、'美女'、'游戏'、'动漫'、'影视'、'明星'、'汽车'、'动物'、'人物'、'美食'、'宗教'、'背景'\n>>>").strip())

    if category not in ['热度','风景','美女','游戏','动漫','影视','明星','汽车','动物','人物','美食','宗教','背景']:
        print('输入有误')
    else:

        page = 1

        WallParper(page, category)()

        if category == '美女':
            print('老色批，美女壁纸下载好了~ 坏笑.jpg')
        else:
            print('下载完毕~')

        input('輸入任意键结束')