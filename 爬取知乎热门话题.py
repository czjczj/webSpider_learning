# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 10:51:41 2019

@author: czj
"""

#爬取知乎热门话题
import requests
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
#创建请求头(反爬虫)
header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

response = requests.get(url,headers=header)
html = response.text

#pyquery数据处理
doc = pq(html)
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text()
    
    #打开文件
    file = open('explore.txt','a',encoding='utf-8')
    file.write('\n'.join([question,author,answer]))
    file.write('\n'+'='*50+'\n')
    file.close()