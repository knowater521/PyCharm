#!-*-coding:utf-8 -*-
#!python3.7
#!@Author：fuq666@qq.com
#!Filename:https://www.umei.fun/
#网址需开ip代理才能访问
#部分网页需要登陆账号才可查看

import requests
import re,os,time,random
from bs4 import BeautifulSoup
from threading import Thread
from atexit import register

#url为待爬取页面的网址，url1为图片对应的显示网址，而不是图片本身的网址
def get_response(url,url1='https://www.umei.fun/'):
    headers = {
        'Referer':url1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    return response

#得到title名
def get_title_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    c = soup.select('.container .row')
    title = c[0].select('h2')[0].get_text()
    return title

#找出当前页面的图片的url
def get_photourl(html):
    photo_urls = []
    soup = BeautifulSoup(html,'html.parser')
    c = soup.select('.container .row')[0]
    imgs = c.select('.card img')
    for img in imgs:
        src = img['src']
        photo_urls.append(src)
    print('一共有{}张图片'.format(len(photo_urls)))
    return photo_urls

#选择保存地址(以title作为文件夹名)
def select_path(path,title):
    path = path + '\\' + title
    if os.path.exists(path):
        path = path + '\\'
    else:
        os.makedirs(path)
        path = path + '\\'
    return path

#保存图片
def save(response,path,n):
    with open(path + '{}.jpg'.format(n),'wb') as f:
        f.write(response.content)

#保存一张图片的流程（用于多线程）
def everyone(photo_url,path,n):
    response = get_response(photo_url)
    save(response, path, n)
    print('{}已保存，{}'.format(n,time.ctime()))

#打印html文本，用于检验
def _html(html):
    with open('C:\\Users\\15394\\Pictures\\爬虫\\umei\\umei_html.txt','w+') as f:
        f.write(html)

def _main(start_url,path):
    print('准备下载：{}'.format(start_url))
    html = get_response(start_url).text
    # _html(html)
    title = get_title_page(html)
    if title == '欢迎回来':     #需要登陆的情况
        num_pattern = re.compile(r'.*?(\d+)')
        num = re.findall(num_pattern,start_url)
        title = '{} 未下载'.format(num[0])
    else:
        num_pattern = re.compile(r'.*?(\d+)')
        num = re.findall(num_pattern, start_url)
        title = num[0] + ' ' + title
    pages = 1
    path = select_path(path,title)
    n = 0
    for i in range(1,int(pages)+1):
        #只有一页，所以html可重用
        photo_urls = get_photourl(html)
        #多线程
        threads = []
        for photo_url in photo_urls:
            n += 1
            t = Thread(target=everyone,args=(photo_url,path,n))     #对每个title内的多张图片使用多线程
            threads.append(t)
        for i in range(len(threads)):
            threads[i].start()              #开始线程
        for i in range(len(threads)):
            threads[i].join()               #可不使用
        #单线程
        # for photo_url in photo_urls:
        #     n += 1
        #     everyone(photo_url,path,n)
        #     for t in range(random.randint(1,3)):
        #         time.sleep(t)

@register
def _atexit():      #注册一个退出函数，在程序退出时执行。（注意：需要提前导入该模块）
    print('结束时间：{}'.format(time.ctime()))
    print('\nDone')

if __name__ == '__main__':
    # start_url = ''
    # path = 'C:\\Users\\15394\\Pictures\\爬虫\\umei'
    # print('开始时间：{}'.format(time.ctime()))
    # _main(start_url, path)
    with open('umei网址.txt','r') as f:
        start_urls = f.readlines()
    for i in start_urls[15:]:
        start_url = i
        path = 'C:\\Users\\15394\\Pictures\\爬虫\\umei'
        print('开始时间：{}'.format(time.ctime()))
        _main(start_url,path)