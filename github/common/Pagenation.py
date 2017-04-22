#!python3
#encoding
import requests
import furl
import time
class Pagenation:
    def __init__(self, request_param):
        self.req = request_param

    def pagenate(self, r, res):
        print("num {0}".format(len(res)))
        print(r.links)
        if "next" in r.links.keys():
            print(r.links["next"]["url"])
            params = self.req.update_otp()
            if "params" in params:
                del params["params"]
            r2 = requests.get(r.links["next"]["url"], **params)
            res += r2.json()
            print("  num {0}".format(len(r2.json())))
            print("sum num {0}".format(len(res)))
            time.sleep(2)
            self.pagenate(r2, res)
        print("all num {0}".format(len(res)))
        return res

    def get_next_page(self, r):
        self.__get_page('next')
    def get_last_page():
        self.__get_page('last')
    def get_prev_page():
        self.__get_page('prev')
    def get_first_page():
        self.__get_page('first')
    def __get_page(self, rel):
        if not(rel in r.links.keys()):
            return None
        else:
            f = furl(r.links[rel]['url'])
            return f.query['page']
