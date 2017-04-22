#!python3
#encoding:utf-8
import Data
import time
import pytz
import requests
import json
import datetime
import github.common.HttpHeader
import github.common.HttpResponser
class Requester:
    def __init__(self, data):
        self.data = data
        self.header = github.common.HttpHeader.HttpHeader(self.data)
        self.responser = github.common.HttpResponser.HttpResponser(self.data)

    def Licenses(self):
        licenses = []
        url = 'https://api.github.com/licenses'
        r = requests.get(url, headers=self.__GetHttpHeaders())
        licenses += self.__ReturnResponse(r, success_code=200)
        next = self.responser.GetLinkNext(r)
        while (None is not next):
            r = requests.get(next, headers=self.__GetHttpHeaders())
            licenses += self.responser.Get(r, success_code=200)
            next = self.responser.GetLinkNext(r)
        return licenses

    """
    指定したライセンスの情報を取得する。
    @param  {string} keyはGitHubにおけるライセンスを指定するキー。
    @return {dict}   結果(JSON)
    """
    def License(self, key):
        url = 'https://api.github.com/licenses/' + key
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.responser.Get(r, success_code=200)

    """
    リポジトリのライセンスを取得する。
    @repo_name {string} 対象リポジトリ名
    @return    {dict}   結果(JSON形式)
    """
    def RepositoryLicense(self, repo_name):
        url = 'https://api.github.com/repos/{0}/{1}'.format(self.data.get_username(), repo_name)
        r = requests.get(url, headers=self.__GetHttpHeaders())
        return self.responser.Get(r, success_code=200)

    """
    def __GetHttpHeaders(self):
        headers = self.header.get()
        headers["Accept"] = "application/vnd.github.drax-preview+json"
        return headers

    def __ReturnResponse(self, r, success_code=None, sleep_time=2, is_show=True):
        if is_show:
            print("HTTP Status Code: {0}".format(r.status_code))
            print(r.text)
        time.sleep(sleep_time)
        if None is not success_code:
            if (success_code != r.status_code):
                raise Exception('HTTP Error: {0}'.format(r.status_code))
                return None
        return json.loads(r.text)
    
    def __BoolToInt(self, bool_value):
        if True == bool_value:
            return 1
        else:
            return 0

    def __ArrayToString(self, array):
        ret = ""
        for v in array:
            ret = v + ','
        return ret[:-1]
    """
