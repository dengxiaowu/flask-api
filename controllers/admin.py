import re

from controllers.base import Base
from flask import request
from library.helper import get_password, varify_password
from library.tokenmanager import TokenManager
from models.admin import AdminModel


class Admin(Base):

    def __init__(self):
        super().__init__()

    # 注册管理账号
    def add_admin(self):

        username = request.values.get('username', '')
        password = request.values.get('password', '')
        mobile = request.values.get('mobile', '')
        (checkRes, checkMessage) = self.check_admin_input(username, password, mobile)
        if not checkRes:
            return self.ret_json(10001, checkMessage)

        model = AdminModel()
        if model.check_user_isvalid(mobile):
            return self.ret_json(10002, '用户已存在')
        else:
            ret = model.add_admin_model(username, mobile, get_password(password))
            if not ret:
                return self.ret_json(10003, '注册用户失败')
            else:
                return self.ret_json(1, 'ok', {})

    @staticmethod
    def check_admin_input(username, password, mobile):
        if len(username) == 0 or len(password) == 0:
            return False, '用户和密码不能为空'

        if re.match(r'^\d{11}$', mobile) is None:
            return False, '手机号异常'

        return True, ''

    # 登录
    def admin_login(self):

        password = request.values.get('password', '')
        mobile = request.values.get('mobile', '')

        if mobile == '':
            return self.ret_json(10001, '手机号为空')

        if password == '':
            return self.ret_json(10002, '密码为空')
        # 获取用户信息
        user_info = AdminModel().get_info_by_mobile(mobile)
        if len(user_info) == 0:
            return self.ret_json(10003, '用户不存在')
        else:
            ret = varify_password(password, user_info["password"])
            if ret:
                token = TokenManager().get_token(user_info['id'], mobile)
                data = {'user_id': user_info['id'], 'user_name': user_info['name'], 'token': token}
                return self.ret_json(1, 'ok', data)
            else:
                return self.ret_json(10004, '密码错误')

    # 登出
    def admin_logout(self):
        token = request.values.get('token', '')

        if token == '':
            return self.ret_json(-1, 'token为空')

        # 获取用户信息
        token_info = TokenManager().verify_token(token)
        if token_info is None:
            return self.ret_json(-1, 'token错误')
        else:
            ret = TokenManager().del_token(token)
            if ret:
                return self.ret_json(1, '退出成功')
            else:
                return self.ret_json(10001, '系统错误哦')
