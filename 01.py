import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent

# 通过循环实现多页图片的抓取
for page in range(1, 11):
    # 生成顶层图片列表页的链接
    fst_url = r'https://colorhub.me/search?tag=data&page={}'.format(page)
    # 生成UA（用户代理），用于爬虫请求头的设置
    UA = UserAgent()
    # 向顶层链接发送请求
    fst_response = requests.get(fst_url, headers={'User-Agent': UA.random})
    # 解析顶层链接的源代码
    fst_soup = BeautifulSoup(fst_response.text)
    # 根据HTML的标记规则，返回次层图片详情页的链接和图片名称
    sec_urls = [i.find('a')['href'] for i in fst_soup.findAll(name='div', attrs={'class': 'card'})]
    pic_names = [i.find('a')['title'] for i in fst_soup.findAll(name='div', attrs={'class': 'card'})]
    # 对每一个次层链接做循环
    for sec_url, pic_name in zip(sec_urls, pic_names):
        # 生成UA，use for spider request head
        UA = UserAgent()
        ua = UA.random
        # 向次层链接发送请求
        sec_response = requests.get(sec_url, headers={'User-Agent': ua})
        # 解析次层链接的源代码
        sec_soup = BeautifulSoup(sec_response.text)
        # return the link of pictures according to the rule mark of HTML
        pic_url = 'https:' + sec_soup.find('img', {'class': 'card-img-top'})['src']
        # send request to the link of pictures
        pic_response = requests.get(pic_url, headers={'User-Agent': ua})
        # 将二进制的图片数据写入到本地（即存储图片到本地）

        with open(pic_name + '.jpg', mode='wb') as fn:
            fn.write(pic_response.content)

        # 生成随机秒数，用于也没的停留
        seconds = random.uniform(1, 3)
        time.sleep(seconds)
