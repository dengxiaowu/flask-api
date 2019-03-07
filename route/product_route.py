from controllers.product import Product
from flask import Blueprint


bp = Blueprint('product', __name__, url_prefix='/pyapi/product/')


# 产品模块====================================================
# 添加产品
@bp.route('add', methods=['POST', 'GET'])
def product_add():
    return Product().product_add()


# 产品详情
@bp.route('info', methods=['POST', 'GET'])
def product_info():
    return Product().product_info()


# 修改产品
@bp.route('update', methods=['POST', 'GET'])
def product_update():
    return Product().product_update()


# 删除产品
@bp.route('del', methods=['POST', 'GET'])
def product_del():
    return Product().product_del()


# 删除产品
@bp.route('list', methods=['POST', 'GET'])
def product_list():
    return Product().product_list()
