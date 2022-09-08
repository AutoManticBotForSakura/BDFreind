import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
import time

base_url = 'https://xn--ypk-dickintheworld-com-d678ae37jzkza746y.bd-friend.com/'
list_id = 1
page = 1


def url_request(url: str, type: str):
    global list_id
    global page
    res_html = requests.get(url, headers={"User-Agent": str(UserAgent().random)}, timeout=5)
    if res_html.status_code == 200:
        res_html.encoding = "utf-8"
        # soup = BeautifulSoup(res_html.text, "html.parser")
        soup = BeautifulSoup(res_html.text, "lxml")

        name_list = soup.find_all("div", class_="no")
        in_list = soup.find_all("div", class_="in")
        age_list = soup.find_all("div", class_="fen")
        img_list = soup.find_all("div", class_="img-wrap1")
        page_list = soup.find_all("div", class_="topage")
        next_page = soup.find_all('a', text="下一页")

        for i in range(0, len(name_list)):
            # name_list[i].text
            # in_list[i].text
            # age_list[i].text
            img_list[i].img.attrs["src"] = base_url + img_list[i].img.attrs["src"]
            page_list[i].a.attrs["href"] = base_url + page_list[i].a.attrs["href"]
        if not (os.path.exists('./' + type + '/')):
            os.mkdir('./' + type + '/')
        for i in range(0, len(name_list)):
            print("正在下载" + str(list_id) + "个内容")
            pic_type = img_list[i].img.attrs["src"].split(".", -1)
            pic_type = pic_type[len(pic_type) - 1]
            pic_res = requests.get(img_list[i].img.attrs["src"])
            # strtemp = './'+type+'/'+ str(info_name_list[i]) + '    ' + str(info_age_list[i]) + '.jpg'
            if (not (os.path.exists('./' + type + '/' + str(list_id) + str(name_list[i].text) + '    ' + str(
                    age_list[i].text) + '.' + pic_type))):
                with open(('./' + type + '/' + str(list_id) + '    ' + str(name_list[i].text) + '    ' + str(
                        age_list[i].text) + '.' + pic_type).replace('*', ''), 'wb') as f:
                    f.write(pic_res.content)
                with open('./' + type + '/list.txt', 'a', encoding='utf-8') as f:
                    info_page = page_list[i].a.attrs["href"]
                    f.write(
                        "id:" + str(list_id) + "  " + str(name_list[i].text) + "地址：" + str(
                            in_list[i].text) + '个人账号地址：' +
                        str(info_page) + '\n')
                    list_id += 1
            time.sleep(1)

        try:
            if next_page[0].attrs["href"]:
                next_href = base_url + next_page[0].attrs["href"]
                print(type + str(page) + "页下载完成")
                page += 1
                return next_href
        except Exception:
            print(type + "下载完成")
            list_id = 1
            page = 1
            return False

    else:
        print('报错信息,网络代码:' + str(res_html.status_code))


if __name__ == '__main__':
    print("程序开始运行，优先为male")
    b_url = "https://xn--ypk-dickintheworld-com-d678ae37jzkza746y.bd-friend.com/?type=0"
    d_url = "https://xn--ypk-dickintheworld-com-d678ae37jzkza746y.bd-friend.com/?type=1"
    while b_url:
        b_url = url_request(b_url, "female")
    while d_url:
        d_url = url_request(d_url, "male")
    print("程序结束")
