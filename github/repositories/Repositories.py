#!python3
#encoding
import requests
import urllib.parse
import json
#from repo.insert.github.api import Pagenation
from github.common import Pagenation
from github.common import RequestParam
class Repositories:
    def __init__(self, request_param):
        self.req = request_param
        self.page = Pagenation.Pagenation(request_param)
        
    def create(self, name, description=None, homepage=None):
        method = 'POST'
        endpoint = 'user/repos'
        params = self.req.get(method, endpoint)
        params['data'] = json.dumps({"name": name, "description": description, "homepage": homepage})
        print(params)
        r = requests.post(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
        print(r.status_code)
        print(r.text)
        return json.loads(r.text)
        
    def list(self, visibility=None, affiliation=None, type=None, sort='full_name', direction=None, per_page=30):
        if (visibility is None) and (affiliation is None) and (type is None):
            type = 'all'
        self.__raise_param_error(visibility, ['all', 'public', 'private'], 'visibility')
        if not(None is affiliation):
            for a in affiliation.split(','):
                self.__raise_param_error(a, ['owner', 'collaborator', 'organization_member'], 'affiliation')
        self.__raise_param_error(type, ['all', 'owner', 'public', 'private', 'member'], 'type')
        self.__raise_param_error(sort, ['created', 'updated', 'pushed', 'full_name'], 'sort')
        if direction is None:
            if sort == 'full_name':
                direction = 'asc'
            else:
                direction = 'desc'
        else:
            self.__raise_param_error(direction, ['asc', 'desc'], 'direction')

        method = 'GET'
        endpoint = 'user/repos'
        params = self.req.get(method, endpoint)
        params['headers']['Accept'] = 'application/vnd.github.drax-preview+json'
        params['params'] = {}
        if not(None is visibility):
            params['params']["visibility"] = visibility
        if not(None is affiliation):
            params['params']["affiliation"] = affiliation
        if not(None is type):
            params['params']["type"] = type
        if not(None is sort):
            params['params']["sort"] = sort
        if not(None is direction):
            params['params']["direction"] = direction
        if not(None is per_page):
            params['params']["per_page"] = per_page
        print(params)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
        res = self.page.pagenate(r, r.json())
        print(r.status_code)
        return res

    def __raise_param_error(self, target, check_list, target_name):
        if not(target is None) and not(target in check_list):
            raise Exception("Parameter Error: [{0}] should be one of the following values. : {1}".format(target_name, check_list))

    """
    @param [int] since is repository id on github.
    """
    def list_public_repos(self, since, per_page=30):
        method = 'GET'
        endpoint = 'repositories'
        params = self.req.get(method, endpoint)
        params['params'] = json.dumps({"since": since, "per_page": per_page})
        print(params)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
        res = self.page.pagenate(r, r.json())
        print(r.status_code)
        print(len(res))
        return res

    def list_languages(self, repo_name):
        method = 'GET'
        endpoint = 'repos/:owner/:repo/languages'
        params = self.req.get(method, endpoint)
        endpoint = 'repos/{0}/{1}/languages'.format(self.req.get_username(), repo_name)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
        if 300 <= r.status_code:
            print(r.status_code)
            print(r.text)
            raise Exception("HTTP Error {0}".format(r.status_code))
            return None
        else:
            return json.loads(r.text)
