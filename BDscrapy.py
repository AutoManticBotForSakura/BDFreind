import requests
from bs4 import BeautifulSoup
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'}


def init(proxy_url: str, download_location: str):
    """
    :param proxy_url: str
    :param download_location: str
    :return: void
    """
    # 检测是否需要代理
    if proxy_url:
        proxies = {'http': proxy_url, 'https': proxy_url}
    else:
        proxies = {'http': ''}
    # 定义page
    page = 1
    # 获取end_page
    end_page_res = requests.get(
        'https://xn--ypk-dickintheworld-com-d678ae37jzkza746y.bd-friend.com/?sort=1&type=0&page=1', proxies=proxies,
        headers=headers)
    end_page_soup = BeautifulSoup(end_page_res.content, 'html.parser')
    end_page_str = end_page_soup.select('body > div.bg > div.page > ul > li.active.visible-xs > span')
    # 获取end_page页数
    end_page = int(str(end_page_str[0].text).split('/')[1])
    # print(end_page)

    if download_location == '':
        download_location = './downloads/'
    # 检测路径是否存在,没有则创建路径
    if not os.path.exists(download_location):
        os.mkdir(download_location)

    # 循环获取内容
    while page <= end_page:
        print('正在爬取第' + str(page) + '页')
        # 定义基址base_url
        base_url = 'https://xn--ypk-dickintheworld-com-d678ae37jzkza746y.bd-friend.com/?sort=1&type=0&page=' + str(page)

        # 获取requests内容
        total_res = requests.get(base_url, proxies=proxies, headers=headers)

        # 使用bs4解析内容
        soup = BeautifulSoup(total_res.content, 'html.parser')
        a_list = soup.select('div.binfo> div.topage > a')
        # print(a_list)
        # print(a_list[0].get('href'))
        for index in range(0, len(a_list)):
            # print(a_list[index].get('href'))
            get_content(a_list[index].get('href'), proxy_url, download_location)
            # 爬虫休眠1秒
            time.sleep(1)
        page += 1

    print("爬虫完成")


def get_content(uri, proxy_url, download_location: str):
    """
    :param uri: str
    :param proxy_url: str
    :param download_location: str
    :return:
    """

    # 部分初始化数据
    base_url = 'https://xn--ypk-dickintheworld-com-d678ae37jzkza746y.bd-friend.com/'
    content_url = base_url + uri

    if proxy_url:
        proxies = {'http': proxy_url, 'https': proxy_url}
    else:
        proxies = {'http': ''}

    try:
        content_res = requests.get(content_url, proxies=proxies, headers=headers)
        soup = BeautifulSoup(content_res.content, 'html.parser')
        nick_name = \
            soup.select('#viewer > div:nth-child(1) > li > p:nth-child(3)')[0].text.split("：")[1]
        age = \
            soup.select('#viewer > div:nth-child(1) > li > p:nth-child(4)')[0].text.split("：")[1]
        location = \
            soup.select('#viewer > div:nth-child(1) > li > p:nth-child(5)')[0].text.split("：")[1]
        height = \
            soup.select('#viewer > div:nth-child(1) > li > p:nth-child(6)')[0].text.split("：")[1]
        weight = \
            soup.select('#viewer > div:nth-child(1) > li > p:nth-child(7)')[0].text.split("：")[1]
        print(nick_name + '基本信息获取成功')
        image_list = soup.select('#viewer.mybox>div')  # 排除第一个
        print('图片列表获取完毕')

        (province, city) = (location.split('，')[0], location.split('，')[1])

        save_url = download_location + province + '/' + city + '/' + nick_name + '/'

        if not os.path.exists(download_location + province):
            os.mkdir(download_location + province)

        if not os.path.exists(download_location + province + '/' + city):
            os.mkdir(download_location + province + '/' + city)

        if not os.path.exists(download_location + province + '/' + city + '/' + nick_name):
            os.mkdir(download_location + province + '/' + city + '/' + nick_name)

        with open(save_url + nick_name + '.txt', 'a', encoding='utf-8') as f:
            f.write(
                "昵称:" + nick_name + '\n年龄:' + age + '\n地区:' + location + '\n身高:' + height + '\n体重:' + weight)
        print(nick_name + '基本信息保存完成')

        for i in range(1, len(image_list)):
            image_url = soup.select('#viewer.mybox>div')[i].select('img')[0].get('src')
            image_bytes = requests.get(image_url, proxies=proxies).content
            # 存储到本地
            if not os.path.exists(save_url + nick_name + str(i) + '.' + image_url.split('.')[-1]):
                with open(save_url + nick_name + str(i) + '张.' + image_url.split('.')[-1], 'wb') as f:
                    f.write(image_bytes)
                    print(nick_name + '第' + str(i) + '张图片保存完成')
                    # 用于爬虫休眠
                    time.sleep(500)

    except Exception as e:
        print('在获取' + uri + '时发生错误', e)


if __name__ == '__main__':
    proxy = input('请输入代理ip或直接回车不开启代理: ')  # 用户选择是否需要代理,直接回车不开启代理
    download_location = input('请输入保存图片的文件夹路径: ')
    init(proxy, download_location)  # 调用初始化函数
