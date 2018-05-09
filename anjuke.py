import conn
import requests
import re
import time

from bs4 import BeautifulSoup
from PIL import Image


# 获取html代码
def get_html_text(url):
    try:
        headers = {
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # 把编码改为utf-8
        return response.content
    except:
        return 'Error!'


# 获取二手房列表
def get_second_hand_house_list(page):
    url = 'https://cs.anjuke.com/sale/p' + str(page)
    html = get_html_text(url)
    second_hand_house_list = parse_second_hand_house_html(html)
    return second_hand_house_list


# 存储二手房列表
def save_second_hand_house(house):
    exists = exists_second_hand_house(house['house_code'])
    if not exists:
        conn.house.insert(house)


# 判断该二手房是否已经存在
def exists_second_hand_house(house_code):
    # print(house_code)
    house_count = conn.house.count({'house_code': house_code})
    if house_count > 0:
        return True
    else:
        return False


# 解析二手房html代码
def parse_second_hand_house_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    house_list = soup.find_all('li', class_='list-item')
    houses_info = []
    for house in house_list:
        house_href = ''
        house_code = ''
        house_address = ''
        house_guarantee = ''

        house_unit_price = house.find('span', class_='unit-price').text
        house_price = house.find('span', class_='price-det').text
        house_title = house.find('a', class_='houseListTitle').text
        if house.find('a', class_='houseListTitle'):
            house_href = house.find('a', class_='houseListTitle')['href']
            r = r'com/prop/view/(.*?)\?'
            house_code = re.findall(r, house_href)[0]
        if house.find('em', class_='guarantee_icon1'):
            house_guarantee = house.find('em', class_='guarantee_icon1')['title']
        house_details = house.find('div', class_='details-item').text
        if house.find('span', class_='comm-address'):
            house_address = house.find('span', class_='comm-address').text
        house_img = house.find('div', class_='item-img').img['src']
        tags = []
        for tag in house.find_all('span', class_='item-tags'):
            tags.append(tag.text)
        house_tags = tags
        house_info = {
            'house_code': house_code,
            'house_unit_price': "".join(house_unit_price.split()),
            'house_price': "".join(house_price.split()),
            'house_tags': house_tags,
            'house_details': "".join(house_details.split()),
            'house_address': "".join(house_address.split()),
            'house_title': "".join(house_title.split()),
            'house_href': house_href,
            'house_img': "".join(house_img.split()),
            'house_guarantee': "".join(house_guarantee.split())
        }
        # print(house_info)
        houses_info.append(house_info)
    return houses_info


# 检验是否需要验证码
def need_identifying_code(html):
    if 1 == 1:
        return False
    return True


# 识别验证码
def detection_identifying_code(img):
    im = Image.open(img)
    return 1234


# 主程序
def main():
    i = 1
    dep = 50
    while i <= dep:
        second_hand_house_list = get_second_hand_house_list(i)
        for j in second_hand_house_list:
            # 判断是否已经保存
            if 1 == 1:
                save_second_hand_house(j)
        print(i)
        time.sleep(2)
        i += 1


if __name__ == '__main__':
    main()

    # file = open('a.txt', 'r', encoding= 'utf-8')
    # f = file.read()
    # # print(f)
    # soup = BeautifulSoup(f, 'html.parser')
    # tags = []
    # tmp_tags = soup.find('div', class_='item-img').img['src']
    # print(tmp_tags)

    # house_href = 'https://cs.anjuke.com/prop/view/A1099653615?from=filter&spread=commsearch_p&position=113&kwtype=filter&now_time=1517304360'
    # r = r'com/prop/view/(.*?)\?'
    # house_code = re.findall(r, house_href)[0]
    # print(house_code)

    # a = exists_second_hand_house('A1075777191')
    # if not a:
    #     print(a)
