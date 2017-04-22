class HttpHeader:
    def __init__(self, data):
        self.data = data
    def Get(self):
        return {
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.data.get_access_token())
        }

