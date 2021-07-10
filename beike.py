import requests
from lxml import etree
import json
import time
import re

url_getPageNum = 'https://cd.ke.com/ershoufang/chenghua'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
}
resp = requests.get(url=url_getPageNum, headers=headers).text
_element = etree.HTML(resp)
page = json.loads(_element.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0])["totalPage"]
print(page)

city = 'chenghua'
infoList = []
for i in range(10):
    url = 'https://cd.ke.com/ershoufang/{0}/pg{1}/'.format(city, i+1)
    print(url)
    resp = requests.get(url=url, headers=headers).text
    _element = etree.HTML(resp)
    tags = _element.xpath('//li/div[@class="info clear"]')
    for tag in tags:
        infoDic = {}
        address = tag.xpath('./div[2]/div[1]/div/a/text()')[0]
        info = tag.xpath('./div/div[@class="houseInfo"]/text()')
        info = info[1].replace(' ', '').split('\n')
        for j in info:
            if '' in info:
                info.remove('')

        floor = info[0]
        totalFloor = int(re.search("共(.*?)层", (info[1])).group(1))
        infoDic['totalFloor'] = totalFloor
        if len(info) == 5:
            year = re.search("\|(.*?)年建\|", (info[2])).group(1)
        else:
            year = ''
        infoDic['year'] = year
        area = float(re.search("\|(.*?)平米", (info[-2])).group(1))
        infoDic['area'] = area
        roomType = re.search("(.*?)\|", (info[-2])).group(1)
        infoDic['roomType'] = roomType
        direction = info[-1].replace('|', '')
        infoDic['direction'] = direction

        totalPrice = float(tag.xpath('./div[2]/div[5]/div[1]/span/text()')[0].replace(' ', ''))
        meterPrice = tag.xpath('./div[2]/div[5]/div[2]/span/text()')[0]
        meterPrice = float(re.search("单价(.*?)元/平米", meterPrice).group(1))
        infoDic['totalPrice'] = totalPrice
        infoDic['meterPrice'] = meterPrice
        infoList.append(infoDic)

    time.sleep(1)
print(infoList, len(infoList))
