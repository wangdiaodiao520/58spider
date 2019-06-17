import re
import requests
from lxml import etree
from settings import UA


class Parse():
    def __init__(self,html):
        self.html = html
        self.page = etree.HTML(html)

    def judge(self):
        if '验证' in self.html:
            return '验证'
        else:
            title = ''.join(self.page.xpath('/html/head/title/text()'))
            if '图' in title:
                if 'starttime' in self.html:
                    return self.parse_data()
                else:
                    return self.parse_data_pc()
            else:
                return self.pares_list()

    def pares_list(self):
        urls = self.page.xpath('//ul[@class="esf-list"]/li/@infoid')
        return urls

    def parse_data(self):
        item = {}
        try:
            item['name'] = re.findall('.*?】(.*?),',''.join(self.page.xpath('//head/title/text()')),re.S)[0]
        except:
            item['name'] = ''
        item['area'] = ''.join(self.page.xpath('//h2[@class="dist-title"]/text()')).replace('小区：','')
        item['address'] = ','.join(self.page.xpath('//div[@class="map-bar"]/ul//li/text()')).replace(' ','').replace('\n','')
        item['name_p'] = ''.join(self.page.xpath('//h2[@class="agent-title"]/text()'))
        item['phone'] = ''.join(self.page.xpath('//p[@class="agent-info highlight"]/text()'))
        item['company'] = ''.join(self.page.xpath('//div[@class="brokencard"]/p/text()')).replace(' ','').replace('\n','').replace('所属公司：','')
        meta = ''.join(self.page.xpath('//head/meta[@name="description"]/@content'))
        try:
            item['price'] = re.findall('售价：(.*?)；', meta, re.S)[0]
        except:
            item['price'] = ''
        try:
            item['property'] = re.findall('产权：.*?（(.*?)）.*?；', meta, re.S)[0]
        except:
            item['property'] = ''
        item['room_hx'] = ''.join(self.page.xpath('//div[@class="size-bar"]/div[last()-1]/p[last()]/text()')).replace(' ','').replace('\n','')
        item['room_mj'] = ''.join(self.page.xpath('//div[@class="size-bar"]/div[last()]/p[last()]/text()')).replace(' ','').replace('\n','')
        item['room_lc'] = ''.join(self.page.xpath('//table[@class="detail-table"]/tr[2]/td[1]/span/text()'))
        item['room_cx'] = ''.join(self.page.xpath('//table[@class="detail-table"]/tr[2]/td[2]/span/text()'))
        item['room_lx'] = ''.join(self.page.xpath('//table[@class="detail-table"]/tr[3]/td[1]/span/text()'))
        item['room_zx'] = ''.join(self.page.xpath('//table[@class="detail-table"]/tr[3]/td[2]/span/text()'))
        item['room_nd'] = ''.join(self.page.xpath('//table[@class="detail-table"]/tr[4]/td[1]/span/text()'))
        item['room_time'] = ''.join(self.page.xpath('//table[@class="detail-table"]/tr[1]/td[2]/span/text()'))
        return item

    def parse_data_pc(self):
        item = {}
        try:
            item['name'] = re.findall('.*?】(.*?),', ''.join(self.page.xpath('//head/title/text()')), re.S)[0]
        except:
            item['name'] = ''
        item['area'] = ''.join(self.page.xpath('//ul[@class="house-basic-item3"]/li[1]/span//text()')).replace(' ','').replace('\n','').replace('小区：','')
        item['address'] = ''.join(self.page.xpath('//ul[@class="house-basic-item3"]/li[2]/span//text()')).replace('\n','').replace(' ', '').replace('地图', '').replace('位置：', '')
        try:
            item['name_p'] = re.findall('userName":"(.*?),',self.html,re.S)[0].encode('utf-8').decode('unicode_escape').strip('"')
        except:
            item['name_p'] = ''
        item['phone'] =  ''.join(self.page.xpath('//p[@class="phone-num"]/text()'))
        item['company'] = ''
        meta = ''.join(self.page.xpath('//head/meta[@name="description"]/@content'))
        try:
            item['price'] = re.findall('售价：(.*?)；', meta, re.S)[0]
        except:
            item['price'] = ''
        try:
            item['property'] = re.findall('产权：.*?（(.*?)）.*?；', meta, re.S)[0]
        except:
            item['property'] = ''
        item['room_hx'] = ''.join(self.page.xpath('//p[@class="room"]/span[@class="main"]/text()')).replace(' ','').replace('\n','')
        item['room_mj'] = ''.join(self.page.xpath('//p[@class="area"]/span[@class="main"]/text()')).replace(' ','').replace('\n','')
        item['room_lc'] = ''.join(self.page.xpath('//p[@class="room"]/span[@class="sub"]/text()')).replace(' ','').replace('\n','')
        item['room_cx'] = ''.join(self.page.xpath('//p[@class="toward"]/span[@class="main"]/text()')).replace(' ','').replace('\n','')
        try:
            item['room_lx'] = re.findall('类型：(.*?) null', meta, re.S)[0]
        except:
            item['room_lx'] = ''
        try:
            item['room_zx'] = re.findall('装修：(.*?)修', meta, re.S)[0]
        except:
            item['room_zx'] = ''
        try:
            item['room_nd'] = re.findall('产权：.*?（(.*?)；', meta, re.S)[0].split('）')[1]
        except:
            item['room_nd'] = ''
        item['room_time'] = ''
        return item




def get_phone(url):
    rep = requests.get(url,headers=UA)
    html = etree.HTML(rep.text)
    phone = ''.join(html.xpath('//p[@class="phone-num"]/text()'))
    return phone




































