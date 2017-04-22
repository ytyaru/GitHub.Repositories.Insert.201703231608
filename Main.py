#!python3
#encoding:utf-8
import os.path
import getpass
import Data
import command.repositories.Inserter
import github.common.RequestParam
import github.repositories.Languages
class Main:
    def __init__(self, user_name, path_db_account, path_db_repo, path_db_license, path_db_api):
        self.data = Data.Data(user_name, path_db_account, path_db_repo, path_db_license)
        self.request_param = github.common.RequestParam.RequestParam(path_db_account, path_db_api, user_name)
        self.inserter = command.repositories.Inserter.Inserter(self.data)

    def Initialize(self):
        self.inserter.Insert(self.request_param)
#        lang = github.repositories.Languages.Languages(db_path_repo, request_param)
#        lang.update_local_db()

    """
    def Initialize(self):
        path_this_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(path_this_dir, "OtherRepositoryUrl.txt")
        with open(file_path, mode="r", encoding="utf-8") as f:
            url = True
            while url:
                url = f.readline().rstrip('\r\n')
                print(url)
                if len(url) == 0:
                    continue
                username = self.data.get_other_username(url)
                repo_name = self.data.get_other_repo_name(url)
                print("ユーザ名: " + username)
                print("リポジトリ名: " + repo_name)
                self.inserter.Insert(username, repo_name)
    """
    def Run(self):
        print('GitHubリポジトリ情報を取得します。')
        url = 'start'
        while '' != url:
            print('GitHubリポジトリのURLを入力してください。(未入力+Enterで終了)')
            print('サブコマンド    l:既存リポジトリ')
            url = input()
            if '' == url:
                break
            elif 'l' == url or 'L' == url:
                self.inserter.Show()
            else:
                username = self.data.get_other_username(url)
                repo_name = self.data.get_other_repo_name(url)
                print("ユーザ名: " + username)
                print("リポジトリ名: " + repo_name)
                # 未登録ならDBへ挿入する（GitHubAPIでリポジトリ情報、言語情報、ライセンス情報を取得して）
                self.inserter.Insert(username, repo_name)


if __name__ == "__main__":
    github_user_name = 'ytyaru'
    os_user_name = getpass.getuser()
    device_name = 'some_device'
    path_db_base = 'db/GitHub'
    path_db_account = '/media/{0}/{1}/{2}/GitHub.Accounts.sqlite3'.format(os_user_name, device_name, path_db_base)
#    path_db_other_repo = './GitHub.Repositories.__other__.sqlite3'.format(os_user_name, device_name, path_db_base)
    path_db_repo = './GitHub.Repositories.{3}.sqlite3'.format(os_user_name, device_name, path_db_base, github_user_name)
    path_db_license = './GitHub.Licenses.sqlite3'.format(os_user_name, device_name, path_db_base)
    path_db_api = '/media/{0}/{1}/{2}/public/v0/GitHub.Apis.sqlite3'.format(os_user_name, device_name, path_db_base)
    main = Main(github_user_name, path_db_account, path_db_repo, path_db_license, path_db_api)
#    main.Run()
    main.Initialize()

