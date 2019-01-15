# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 18:02:45 2019

@author: czj
"""

#爬取今日头条街拍照片
import urllib
import requests
import json
import os
import time

base_url = "https://www.toutiao.com/search_content/?"
headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        "X-Requested-with":"XMLHttpRequest",
        'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D'
}
img_path = "G:\\B题全部数据\\img"
def get_one_page(offset):
    params = {
            "offset":offset,
            'format':'json',
            'keyword':'街拍',
            'autoload':'true',
            'count':20,
            'cur_tab':1,
            'from':'search_tab',
            'pd':'synthesis'
    }
    
    param = urllib.parse.urlencode(params)
    url = base_url+param
    
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print("%i 个Json连接Error"%((offset/20)+1))

def save_images(title, image_list):
    path = os.path.join(img_path,title)
    if not os.path.exists(path):
        os.mkdir(path)
    #获取图片url_list
    img_url_list = ['https:'+url.get('url') for url in image_list]
    img_name_list = [url.get('url').split('/')[-1]for url in image_list]
    
    for i in range(len(img_url_list)):
        response = requests.get(img_url_list[i],headers=headers)
        imgPath = path+'\\'+img_name_list[i]+'.jpg'
        if not os.path.exists(imgPath):
            with open(imgPath,'wb') as f:
                f.write(response.content)
                f.close()
            time.sleep(3)
        
def parse_one_page(json):
    items = json.get('data') 
    if items:    
        for item in items:
            title = item.get("title")
            image_list = item.get("image_list")
            image_count = item.get("image_count")
            if title and image_list and image_count:
                print("正在保存 '%s',共%d张图片....."%(title, image_count))
                save_images(title, image_list)
def main():
    #获取前十次的图片
    for i in range(3):
        offset = i*20
        json = get_one_page(offset)
        print("==================第%d个Json文件==============="%(i+1))
        parse_one_page(json)
        time.sleep(5)
        print("==================第%d个Json保存完毕==============="%(i+1))
    print("Successful")

main()