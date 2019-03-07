from controllers.account import Account
from flask import Blueprint

bp = Blueprint('account', __name__, url_prefix='/pyapi/account/')


# 账号========================================================
# 添加账号信息
@bp.route('add', methods=['POST', 'GET'])
def account_add():
    return Account().account_add()


# 账号信息详情列表（在客户基本信息中）
@bp.route('list', methods=['POST', 'GET'])
def account_list():
    return Account().account_list()


# 账号信息详情
@bp.route('info', methods=['POST', 'GET'])
def account_info():
    return Account().account_info()


# 修改账号信息
@bp.route('update', methods=['POST', 'GET'])
def account_update():
    return Account().account_update()


# 删除账号信息
@bp.route('del', methods=['POST', 'GET'])
def account_del():
    return Account().account_del()
