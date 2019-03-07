from controllers.common import Common
from controllers.upload import Upload
from flask import Blueprint

bp = Blueprint('common', __name__, url_prefix='/pyapi/')


# ======================= common ============================
# 文件上传
@bp.route('upload', methods=['POST', 'GET'])
def upload():
    return Upload().upload_file()


# 资产类型列表
@bp.route('assets_type_list', methods=['POST', 'GET'])
def assets_type_list():
    return Common().assets_type_list()


# 交易所列表
@bp.route('exchange_list', methods=['POST', 'GET'])
def exchange_list():
    return Common().exchange_list()
