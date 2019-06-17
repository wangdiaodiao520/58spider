from queue import Queue
from city import citylist
from crawler import Crawler
from settings import ESF_M_DATA,ESF_M_LIST,ESF_P_M_LIST,ESF_P_DATA
import time

class Spider():
    def __init__(self,city,point):
        self.point = point#启动函数判定输入
        self.city = citylist[city]
        self.q_url = Queue(maxsize=0)
        self.q_data = Queue(maxsize=0)

    def get_data(self):
        if self.point == "二手房":
            list_offset_url = ESF_M_LIST
            data_offset_url = ESF_M_DATA
        elif self.point == "个人二手房":
            list_offset_url = ESF_P_M_LIST
            data_offset_url = ESF_P_DATA
        else:
            pass
        urls = [list_offset_url.format(city=self.city, num=i) for i in range(101)]
        for url in urls:
            Crawler([url], self.q_url, self.q_data).main()
            data_urls = [data_offset_url.format(city=self.city, bm=self.q_url.get()) for _ in range(self.q_url.qsize())]
            for i in range(0, len(data_urls), 4):
                data_url = data_urls[i:i + 4]
                Crawler(data_url, self.q_url, self.q_data).main()
                for _ in range(self.q_data.qsize()):
                    print(self.q_data.get())
                time.sleep(5)



#s = Spider('上海','个人二手房').get_data()
s = Spider('北京','二手房').get_data()

