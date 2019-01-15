# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 16:19:49 2019

@author: czj
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 16:13:53 2019

@author: czj
"""

#猫眼Top_100爬取
import requests
import regex as re
import json
import time

def get_one_html(url):
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        return response.text
    return None

def parse_one_html(html):
    #影片排名正则
    a = r"<dd>.*?board-index.*?>(.*?)</i>"
    #匹配影片名称
    a = a + '.*?data-src=\"(.*?)\"'
    #匹配电影名称
    a = a + '.*?class=\"name\">.*?>(.*?)<\/a><\/p>'
    #匹配主演
    a = a + '.*?class=\"star\">\s+主演：(.*?)\s+<\/p>'
    #匹配上映时间
    a = a + ".*?class=\"releasetime\">上映时间：(.*?)<\/p>"
    #匹配影片评分
    a = a + ".*?class=\"score\">.*?>(.*?)<\/i>.*?>(.*?)<\/i>"
    
    pattern = re.compile(a,re.S)
    items = pattern.findall(html)
    for item in items:
        yield{
                'index':item[0],
                'image':item[1],
                'title':item[2].strip(),
                'actor':item[3].strip(),
                'time':item[4].strip(),
                'score':item[5]+item[6]
                }

def write_to_json(content):
    with open('result.txt','a',encoding='utf-8') as f:
#        print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        
def main():
    base_url = "https://maoyan.com/board/4?offset="
    for i in range(10):
        url = base_url + str(i*10)
        print(url)
        
        #获取当前链接页面内容
        html = get_one_html(url)
        #解析当前页面
        items = parse_one_html(html)
        #保存为Json数据
        for item in items:
            print(item)
            write_to_json(item)
        time.sleep(2)
        print('\n')
            
main()

###########################
url = "https://maoyan.com/board/4?offset=0"
r = requests.get(url)
h = r.text
#a = r"<dd>.*?board-index.*?>.*?</i>"
#a = '.*?data-src=\"(.*?)\"'
#影片排名正则
a = r"<dd>.*?board-index.*?>(.*?)</i>"
#匹配影片名称
a = a + '.*?data-src=\"(.*?)\"'
#匹配电影名称
a = a + '.*?class=\"name\">.*?>(.*?)<\/a><\/p>'
#匹配主演
a = a + '.*?class=\"star\">\s+主演：(.*?)\s+<\/p>'
#匹配上映时间
a = a + ".*?class=\"releasetime\">上映时间：(.*?)<\/p>"
#匹配影片评分
a = a + ".*?class=\"score\">.*?>(.*?)<\/i>.*?>(.*?)<\/i>"

pat = re.compile(a,re.S)
res = pat.findall(h)
