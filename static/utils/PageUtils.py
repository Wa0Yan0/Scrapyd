from flask import jsonify


class PageUtils:
    pageNum = 1
    pageSize = 10
    total = 0

    def __init__(self, total, queryInfo):
        self.queryInfo = queryInfo
        self.pageNum = self.queryInfo['pageNum']
        self.pageSize = self.queryInfo['pageSize']
        self.total = total

    def begin(self):
        return (self.pageNum - 1) * self.pageSize

    def end(self):
        return self.total if (self.pageNum * self.pageSize) > self.total else (self.pageNum * self.pageSize)

    def wrapper(self, data):
        return jsonify([{
            "pageNum": self.pageNum,
            "pageSize": self.pageSize,
            "total": self.total,
            "list": data
        }])
