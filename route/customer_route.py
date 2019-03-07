from controllers.customer import Customer
from controllers.product_plan import ProductPlan
from flask import Blueprint

bp = Blueprint('customer', __name__, url_prefix='/pyapi/customer/')


# 客户模块=====================================================
# 客户列表
@bp.route('list', methods=['POST', 'GET'])
def customer_list():
    return Customer().customer_list()


# 跟进人列表
@bp.route('salesreps', methods=['POST', 'GET'])
def salesrep_list():
    return Customer().salesrep_list()


# 添加客户信息
@bp.route('add', methods=['POST', 'GET'])
def customer_add():
    return Customer().customer_add()


# 客户信息详情（在客户基本信息中）
@bp.route('info', methods=['POST', 'GET'])
def customer_info():
    return Customer().customer_info()


# 修改客户信息
@bp.route('update', methods=['POST', 'GET'])
def customer_update():
    return Customer().customer_update()


# 删除客户
@bp.route('del', methods=['POST', 'GET'])
def customer_del():
    return Customer().customer_del()


# 客户账号列表
@bp.route('account_list', methods=['POST', 'GET'])
def customer_account_list():
    return Customer().customer_account_list()


# 客户账号资产
@bp.route('account_assets', methods=['POST', 'GET'])
def customer_account_assets():
    return Customer().customer_account_assets()


# 资金划转
@bp.route('assets_change', methods=['POST', 'GET'])
def assets_change():
    return Customer().assets_change()


# 平仓申请
@bp.route('closing_apply', methods=['POST', 'GET'])
def closing_apply():
    return Customer().closing_apply()


# 账号待分配余额 对应币种
@bp.route('unallocated_assets', methods=['POST', 'GET'])
def unallocated_assets():
    return Customer().unallocated_assets()


# 客户账号的方案列表-下拉
@bp.route('account_plan_list', methods=['POST', 'GET'])
def account_plan_list():
    return ProductPlan().get_account_plan_list()
