# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 15:14:56 2019

@author: czj
"""

#爬取湖北大学新闻测试 最终版
import urllib
import regex as re
import pymysql
import time

base_imgUrl = r"http://www.hubu.edu.cn"
base_nextLink = r"http://www.hubu.edu.cn/info/1316/"
imgs_save_path = r"G:\\B题全部数据\\img\\"
imgs_count = 1
news_count = 1

def save_newsinfo(news_url,title,aef,tim,img_url,content):
    db = pymysql.connect('localhost','root','','python')
    conn = db.cursor()
    #准备好数据
    insert_title = title
    insert_author = aef[0]
    insert_editor = aef[1]
    insert_source = aef[2]
    insert_time = tim[0]
    insert_imgUrl = ''
    insert_content = ''
    if len(img_url) != 0:
        for img in img_url:
            insert_imgUrl += (base_imgUrl+img+";")
    if len(content) != 0:
        for cont in content:
            insert_content += (cont+";;")
            
    sql = "insert into news(title,author,editor,source,time,imgUrl,content) values ('%s','%s','%s','%s','%s','%s','%s')"%(
            insert_title,insert_author,insert_editor,insert_source,insert_time,insert_imgUrl,insert_content)
    try:
        conn.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("%s Error"%(news_url))
    db.close()
    
def img2disk(img_url):
    global imgs_count
    for iu in img_url:
        url = base_imgUrl+iu+'.jpg'
        img_page = urllib.request.urlopen(url)
        img_data = img_page.read()
        img_name = iu.split('/')[-1]
        f = open(imgs_save_path+img_name+'.jpg','wb')
        f.write(img_data)
        imgs_count += 1 #统计爬取的图片的个数    
        time.sleep(3) #一张图片睡3秒钟
        f.close()   
        
def get_next(news_url):
    page = urllib.request.urlopen(news_url)
    data = page.read().decode("UTF-8")
    data = re.sub(r"\s+",'',data)  #替换掉所有的空格
    
    #匹配新闻标题
    title_regular = r'(?<=<h3>).*?(?=<\/h3>)'
    title_pattern = re.compile(title_regular)
    title = title_pattern.findall(data)[1].replace(u'\u3000',u' ')
    
    #匹配 作者，编辑，来源, 发布时间
    aeft_regular = r'(?<=<i>作者).*?(?=<\/i>)'
    aeft_pattern = re.compile(aeft_regular)
    aeft_raw = aeft_pattern.findall(data)[0]
    pat_aef = re.compile(r'(?<=：).*?(?=&nbsp)')
    pat_time = re.compile(r"\d{4}\/\d{2}\/\d{2}")
    aef = pat_aef.findall(aeft_raw)
    tim = pat_time.findall(aeft_raw)
    
    #匹配图片
    img_regular = r'(?<=<imgwidth=\"\d+\"src=\").*?(?=\.jpg)'
    img_pattern = re.compile(img_regular)
    img_url = img_pattern.findall(data)
    #base_imgUrl = r"http://www.hubu.edu.cn"
    #imgUrl = base_imgUrl+'/__local/E/21/38/4F1D9EA1EDBB4EEE73262E133BF_2191A728_BF7B'+'.jpg'
    
    #获取 下一条链接 
    nextLink_regular = r'(?<=下一条：<ahref=\")\d*\.htm'
    nextLink_pattern = re.compile(nextLink_regular)
    next_link = nextLink_pattern.findall(data)[0]
    
    #匹配新闻主题内容
    content_regular = r'(?<=<spanstyle="font-size:16px">).+?(?=<\/span>)'
    content_pattern = re.compile(content_regular)
    content_tmp = content_pattern.findall(data)
    content = [re.sub(r"<.*?>","",i) for i in content_tmp]

    try:
        #保存当前页面中的图片到本地中
        if len(img_url) != 0:
            img2disk(img_url)      
        
        #将爬取的数据保存到数据库中
        save_newsinfo(news_url,title,aef,tim,img_url,content)
    except:
        print("%s Save Failed"%(news_url))
        
    #返回下一个连接
    return next_link


def main():
#    start_url = "http://www.hubu.edu.cn/info/1316/30164.htm"
#    start_url = "http://www.hubu.edu.cn/info/1316/29718.htm"
    start_url = "http://www.hubu.edu.cn/info/1316/26549.htm"    
    next_link = get_next(start_url)
    save_num = 100
    
    global news_count
    
    while len(next_link) != 0 and (news_count<save_num):
        url = base_nextLink + next_link
        print("第%d个页面 (%s) 正在保存数据库中......"%(news_count+1,url))
        next_link = get_next(url)
        news_count += 1
        time.sleep(4) #一个页面睡四秒钟
    print("end")

if __name__=="__main__":
    main()
