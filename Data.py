#!python3
#encoding:utf-8
import os.path
import subprocess
import dataset
import urllib.parse
class Data:
    def __init__(self, user_name, path_db_account, path_db_other_repo, path_db_license):
        self.user_name = user_name
        self.db_acc = dataset.connect('sqlite:///' + path_db_account)
        self.db_repo = dataset.connect('sqlite:///' + path_db_other_repo)
        self.db_license = dataset.connect('sqlite:///' + path_db_license)
    def get_username(self):
        return self.user_name
    def get_ssh_host(self):
        return "github.com.{0}".format(self.user_name)
    def get_mail_address(self):
        return self.db_acc['Accounts'].find_one(Username=self.get_username())['MailAddress']
    def get_access_token(self, scopes=None):
        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.db_acc['Accounts'].find_one(Username=self.get_username())['Id'])
        if not(None is scopes):
            sql = sql + " AND ("
            for s in scopes:
                sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
            sql = sql.rstrip(" OR ")
            sql = sql + ')'
        return self.db_acc.query(sql).next()['AccessToken']
    def get_repo_name(self):
        return os.path.basename(self.path_dir_pj)
    def get_repo_description(self):
        return self.description
    def get_repo_homepage(self):
        return self.homepage

    def get_other_username(self, urlstring):
        return self.__url_to_names(urlstring)[0]
    def get_other_repo_name(self, urlstring):
        return self.__url_to_names(urlstring)[1]
    def __url_to_names(self, urlstring, is_show=False):
        url = urllib.parse.urlparse(urlstring)
        if is_show:
            print(urlstring)
            print(url.path)
            print(os.path.split(url.path))
            print(os.path.split(url.path[1:]))
            print(self.get_split_pass(url.path[1:]))
        return self.get_split_pass(url.path[1:])
    """
    パスを配列に分解する。
    今回はurllib.parse.urlparse().pathの部分の1番目=user, 2番目=リポジトリ名として取得したい。
    os.path.split()は末尾要素とそれ以前のすべての２つにしか分解されないため使えない。
    https://docs.python.jp/3/library/os.path.html#os.path.split
    パス区切り文字はos.nameで区別する。
    https://docs.python.jp/3/library/os.html#os.name
    """
    def get_split_pass(self, urlstring):
        # Windows('nt')
        if 'nt' == os.name:
            return urlstring.split('\\')
        # Linux,Mac('posix'), Android('java')
        else:
            return urlstring.split('/')

