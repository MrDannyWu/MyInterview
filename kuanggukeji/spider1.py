
import requests
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import csv

url = 'https://www.mcrecycle.com/category/mobile-phones/'

#写入csv文件头部
def save_to_csv():
    with open('data1.csv', 'a', newline='') as csvfile:
        fieldnames = ['date', 'deviceModel', 'provider', 'condition', 'networks', 'quote']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        csvfile.close()


#获取页面源码
def get_html(url):
    header = {
        'Cookie': 'PHPSESSID=7rbn98vlng2b2muuq39tanlab6',
        'Connection': 'keep-alive',
        'Host': 'www.mcrecycle.com',
        'Referer':'https://www.mcrecycle.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    try:
        web_data = requests.get(url,headers=header).text
        return web_data
    except :
        print('Connection Error...')


#获取品牌url
def get_brand_url(web_data):
    soup = BeautifulSoup(web_data,'lxml')
    try:
        items = soup.select('.category-list .category a')
        brand_url_list = []
        for item in items:
            brand_name = item.select('.name')[0].text
            brand_url = item.get('href')
            brand_url_list.append(brand_url)
            print(brand_name)
            print(brand_url)
        return brand_url_list
    except:
        print('css select error...')
        pass

#获取设备详情页的url
def get_phone_url(brand_url):
    phone_url_list = []
    for i in range(11):
        url = brand_url + str(i*16) +'/16/'
        #print(url)
        web_data = get_html(url)
        soup = BeautifulSoup(web_data,'lxml')
        #print(soup)
        device_list = soup.select('.device-list .device a')
        if len(device_list) == 0:
            break
        #print(device_list)
        else:
            print(url)
            for device in device_list:
                phone_url = device.get('href')
                print(phone_url)
                phone_url_list.append(phone_url)
    print(phone_url_list)
    print(len(phone_url_list))
    return phone_url_list

#获取设备的详情数据
def get_phone_detils(phone_url):
    condition_1 = 'null'
    condition_2 = 'null'
    price_condition_1 = 'null'
    price_condition_2 = 'null'
    price_networks_4 = 'null'
    price_networks_12 = 'null'
    price_networks_6 = 'null'
    price_networks_14 = 'null'
    price_networks_15 = 'null'
    price_networks_7 = 'null'
    price_networks_5 = 'null'

    web_data = get_html(phone_url)
    soup = BeautifulSoup(web_data,'lxml')
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    device_model = soup.select('h1')[0].text
    provider = 'MC Recycle'
    condition_list = soup.select('.condition .controls .radio')
    condition = None
    print(condition_list)
    price_networks_list = []
    try:
        condition_1 = soup.select('.option_1_container label')[0].text
    except:
        print('没有condition_1')
        pass
    try:
        condition_2 = soup.select('.option_2_container label')[0].text
    except:
        print('没有condition_2')
        pass
    print(condition_1)
    print(condition_2)
    try:
        price_condition_1 = soup.select('#price_condition_1')[0].get('value')
    except:
        print('没有price_condition_1')
        pass

    try:
        price_condition_2 = soup.select('#price_condition_2')[0].get('value')
    except:
        print('没有price_condition_2')
        pass
    print(price_condition_1)
    print(price_condition_2)
    try:
        price_networks_4 = soup.select('#price_networks_4')[0].get('value')
        price_networks_list.append(price_networks_4)
    except:
        print('没有price_networks_4')
        pass

    try:
        price_networks_12 = soup.select('#price_networks_12')[0].get('value')
        price_networks_list.append(price_networks_12)
    except:
        print('没有price_networks_12')
        pass

    try:
        price_networks_6 = soup.select('#price_networks_6')[0].get('value')
        price_networks_list.append(price_networks_6)
    except:
        print('没有price_networks_6')
        pass

    try:
        price_networks_14 = soup.select('#price_networks_14')[0].get('value')
        price_networks_list.append(price_networks_14)
    except:
        print('没有price_networks_14')
        pass

    try:
        price_networks_15 = soup.select('#price_networks_15')[0].get('value')
        price_networks_list.append(price_networks_15)
    except:
        print('没有price_networks_15')
        pass

    try:
        price_networks_7 = soup.select('#price_networks_7')[0].get('value')
        price_networks_list.append(price_networks_7)
    except:
        print('没有price_networks_7')
        pass

    try:
        price_networks_5 = soup.select('#price_networks_5')[0].get('value')
        price_networks_list.append(price_networks_5)
    except:
        print('没有price_networks_5')
        pass
    print(price_networks_list)
    for other in condition_list:
        if 'checked' in str(other):
            condition = other.select('label')[0].text
            #print(condition)
    networks_list = soup.select('.networks .controls #networks option')
    networks = 'null'
    networks_data_list = []
    for each in networks_list:
        networks_data_list.append(each.text)
    print(networks_data_list)

    if condition_1 is not 'null':
        for x,y in zip(price_networks_list,networks_data_list):
            quote = float(x) + float(price_condition_1)
            data = {
                'date':date,
                'deviceModel':device_model,
                'provider':provider,
                'condition':condition_1,
                'networks':y,
                'quote':quote,
            }
            with open('data1.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['date', 'deviceModel', 'provider', 'condition', 'networks', 'quote']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow(data)
                csvfile.close()
            print(data)
    if condition_2 is not 'null':
        for x,y in zip(price_networks_list,networks_data_list):
            quote = float(x) + float(price_condition_2)
            data = {
                'date':date,
                'deviceModel':device_model,
                'provider':provider,
                'condition':condition_2,
                'networks':y,
                'quote':quote,
            }
            with open('data1.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
                fieldnames = ['date', 'deviceModel', 'provider', 'condition', 'networks', 'quote']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                writer.writerow(data)
                csvfile.close()
            print(data)

#get_phone_detils('https://www.mcrecycle.com/category/mobile-phones/apple/apple-iphone-6-plus-64gb~p97/')
# web_data = get_html1('https://www.mcrecycle.com/category/mobile-phones/apple/apple-iphone-5s-16gb~p65/')
# print(web_data)
# print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) )
def main():
    save_to_csv()
    web_data = get_html('https://www.mcrecycle.com/category/mobile-phones/')
    #print(web_data)
    brand_url_list = get_brand_url(web_data)
    print(brand_url_list)
    phone_url_total = []
    for brand_url in brand_url_list:
        print(brand_url)
        phone_url_list = get_phone_url(brand_url)
        for phone_url in phone_url_list:
            phone_url_total.append(phone_url)
    print(phone_url_total)
    print(len(phone_url_total))
    #pool = Pool(10)
    #pool.map(get_phone_detils,phone_url_total)
    for url in phone_url_total:
        get_phone_detils(url)

if __name__ == '__main__':
    main()
