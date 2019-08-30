#!-*-coding:utf-8 -*-
#!python3.7
#!@Author：fuq666@qq.com
#!Filename:https://www.umei.fun/

#部分网页需要登陆账号才可查看

import requests
import re,os,time,random
from bs4 import BeautifulSoup

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

def main(start_url,path):
    print('准备下载：{}'.format(start_url))
    html = get_response(start_url).text
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
    n = 1
    for i in range(1,int(pages)+1):
        url = start_url
        html = get_response(url).text
        photo_urls = get_photourl(html)
        for photo_url in photo_urls:
            response = get_response(photo_url)
            save(response,path,n)
            print('{}已保存'.format(n))
            for t in range(random.randint(1,3)):
                time.sleep(t)
            n += 1

if __name__ == '__main__':
    start_urls = [
        'https://www.umei.fun/posts/6609',
        'https://www.umei.fun/posts/6492',
        'https://www.umei.fun/posts/6456',
        'https://www.umei.fun/posts/6328',
        'https://www.umei.fun/posts/6490',
        'https://www.umei.fun/posts/7258',
        'https://www.umei.fun/posts/7259',
        'https://www.umei.fun/posts/7260',
        'https://www.umei.fun/posts/7268',
        'https://www.umei.fun/posts/7265',
        'https://www.umei.fun/posts/7272',
        'https://www.umei.fun/posts/7275',
        'https://www.umei.fun/posts/1',
        'https://www.umei.fun/posts/27',
        'https://www.umei.fun/posts/110',
        'https://www.umei.fun/posts/125',
        'https://www.umei.fun/posts/179',
        'https://www.umei.fun/posts/192',
        'https://www.umei.fun/posts/212',
        'https://www.umei.fun/posts/265',
        'https://www.umei.fun/posts/4464',
        'https://www.umei.fun/posts/4254',
        'https://www.umei.fun/posts/4643',
        'https://www.umei.fun/posts/4644',
        'https://www.umei.fun/posts/4782',
        'https://www.umei.fun/posts/4783',
    ]
    # start_url = start_urls[0]
    # path = 'C:\\Users\\15394\\Pictures\\爬虫\\umei'
    # main(start_url, path)
    for i in start_urls[10:]:
        start_url = i
        path = 'C:\\Users\\15394\\Pictures\\爬虫\\umei'
        main(start_url,path)