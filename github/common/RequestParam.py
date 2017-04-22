#!python3
#encoding:utf-8
import os.path
import dataset
#from tkinter import Tk
class RequestParam:
    def __init__(self, db_path_account, db_path_api, username):
        self.username = username
        self.auth_param = RequestParam.AuthParam(db_path_account, db_path_api, username)
        self.params = None

    def get_username(self):
        return self.username

    def get(self, http_method, endpoint):
        params = self.auth_param.get(http_method, endpoint)
        if not("headers" in params.keys()):
            params['headers'] = {}
        params['headers'].update({"Time-Zone": "Asia/Tokyo"})
        if not("Accept" in params['headers'].keys()):
            params['headers'].update({"Accept": "application/vnd.github.v3+json"})
        self.params = params
        return self.params

    def update_otp(self):
        if not(self.params is None):
            if (("headers" in self.params) and ("X-GitHub-OTP" in self.params["headers"])):
                self.params["headers"]["X-GitHub-OTP"] = self.auth_param.get_otp()
        return self.params

    class AuthParam:
        def __init__(self, db_path_account, db_path_api, username):
            self.username = username
            self.db_account = dataset.connect('sqlite:///' + db_path_account)
            self.db_api = dataset.connect('sqlite:///' + db_path_api)

        def get(self, http_method, endpoint):
            params = {}
            account = self.db_account['Accounts'].find_one(Username=self.username)
            api = self.db_api['Apis'].find_one(HttpMethod=http_method, Endpoint=endpoint)
            print(api)
            print(api['Grants'])
            print("type(Grants)1: {0}".format(type(api['Grants'])))
            print("len(Grants)1: {0}".format(len(api['Grants'])))
            print("len(Grants)2: {0}".format(len(api['Grants'].split(","))))
            if ("Token" in api['AuthMethods']):
                token = self.__get_access_token(account['Id'], api['Grants'].split(","))
                params['headers'] = {"Authorization": "token " + token}
            elif ("ClientId" in api['AuthMethods']):
                raise Exception('Not implemented clientId authorization.')
            elif ("Basic" in api['AuthMethods']):
                params['auth'] = (self.username, account['Password'])
                two_factor = self.db_account['TwoFactors'].find(AccountId=account['Id'])
                if not(None is two_factor):
                    """
                    t = Tk()
                    otp = t.clipboard_get()
                    t.destroy()
                    """
                    otp = "some_otp"
                    params['headers'] = {"X-GitHub-OTP": otp}
            else:
                raise Exception('Not found AuthMethods: {0} {1}'.format(api['HttpMethod'], api['Endpoint']))
            return params

        def __get_access_token(self, account_id, scopes):
            sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(account_id)
            if (not(None is scopes) and (0 < len(scopes)) and (0 < len(scopes[0]))):
                sql = sql + " AND ("
                for s in scopes:
                    sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
                sql = sql.rstrip(" OR ")
                sql = sql + ')'
            print(sql)
            tokens = self.db_account.query(sql)
            token = None
            for t in tokens:
               token = t['AccessToken']
            return token

        def get_otp(self):
            account = self.db_account['Accounts'].find_one(Username=self.username)
            two_factor = self.db_account['TwoFactors'].find(AccountId=account['Id'])
            if None is two_factor:
                return None
            else:
                t = Tk()
                otp = t.clipboard_get()
                t.destroy()
                return otp
