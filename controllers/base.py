import json

from flask import Response, request
from library.tokenmanager import TokenManager


class Base:
    def __init__(self):
        self.ret = {}
        self.ok = 1
        self.msg = 'ok'

    def check_token(self):
        token = request.values.get('token', '')
        if token == '':
            return self.ret_json(-1, 'token为空')

        # 获取用户信息
        token_info = TokenManager().verify_token(token)
        if not token_info:
            return self.ret_json(-1, 'token错误或未登录')
        return token_info

    def ret_json(self, status, msg, data={}):
        self.ret['status'] = status
        self.ret['msg'] = msg
        self.ret['data'] = data

        return Response(json.dumps(self.ret), mimetype='application/json')

    def page_info(self, total, current_page, page_size):
        page_info = dict()
        page_info['current_page'] = int(current_page)
        page_info['page_size'] = int(page_size)
        page_info['total'] = int(total)
        return page_info

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
