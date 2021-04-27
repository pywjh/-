import os
import requests
from lxml import etree
from urllib.request import urlretrieve


class WallParper():

    def __init__(self):
        super().__init__()
        self.worklist = []
        self.url = 'http://pic.netbian.com'
        self.session = requests.session()
        self.session.encoding = 'utf-8'
        self.session.get(self.url)
        self.page = 2
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        self.session.headers.update(self.headers)

    def response(self, html):
        return etree.HTML(html)

    def search_img(self, all_page):
        all_page += 1
        for page in range(1, all_page):
            if page == 1:
                url = self.url
            else:
                url = f"{self.url}/index_{page}.html"
            html = self.response(self.session.get(url).text)
            for url in html.xpath('//ul[@class="clearfix"]/li/a/@href'):
                self.worklist.append(f"{self.url}{url}")

    def dowmload_img(self):
        for url in self.worklist:
            response = requests.get(url, headers=self.headers)
            response.encoding = 'GBK'
            html = self.response(response.text)
            src = html.xpath('//a[@id="img"]/img/@src')[0]
            title = html.xpath('//a[@id="img"]/img/@title')[0]
            img_name = f"wallparper/{title}.jpg"
            if img_name not in os.listdir('wallparper'):
                try:
                    urlretrieve(
                        url=f"{self.url}{src}",
                        filename=img_name
                    )
                except Exception:
                    print(f"{img_name} - 下载失败！")
            print(f"{img_name} - 已存在，跳过下载")

    def __call__(self, page):
        self.search_img(page)
        self.dowmload_img()


if __name__ == "__main__":
    WallParper()(10)