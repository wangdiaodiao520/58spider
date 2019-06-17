from settings import UA
from parse import Parse
import requests


class Crawler():
    def __init__(self,url_list,q_url,q_data):
        self.urls = url_list
        self.q_url = q_url
        self.q_data = q_data

    def get_normal(self):
        rep = requests.get(self.urls,headers=UA)
        if rep.status_code == 200:
            res = Parse(rep.text).judge()
            if type(res).__name__ == "list":
                for i in res:
                    self.q_url.put(i)
            elif type(res).__name__ == "dict":
                return res
                #self.q_data.put(res)
            elif type(res).__name__ == 'str':
                return res
            else:
                pass
        else:
            pass





