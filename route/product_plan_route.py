from controllers.product_plan import ProductPlan
from flask import Blueprint


bp = Blueprint('product_plan', __name__, url_prefix='/pyapi/product_plan/')


# ===================================================================
# 添加 产品方案
@bp.route('add', methods=['POST', 'GET'])
def product_plan_add():
    return ProductPlan().product_plan_add()


# 产品方案权益统计
@bp.route('earnings', methods=['POST', 'GET'])
def product_plan_earnings():
    return ProductPlan().product_plan_earnings()


# 产品方案=转账详情
@bp.route('transfer', methods=['POST', 'GET'])
def product_plan_transfer():
    return ProductPlan().product_plan_transfer()


# 产品方案详情
@bp.route('info', methods=['POST', 'GET'])
def product_plan_info():
    return ProductPlan().product_plan_info()


# 修改产品方案
@bp.route('update', methods=['POST', 'GET'])
def product_plan_update():
    return ProductPlan().product_plan_update()


# 删除产品方案
@bp.route('del', methods=['POST', 'GET'])
def product_plan_del():
    return ProductPlan().product_plan_del()


# 产品方案-也是根据客户-分页
@bp.route('list', methods=['POST', 'GET'])
def product_plan_list():
    return ProductPlan().product_plan_list()



