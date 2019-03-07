from controllers.asset import Asset
from flask import Blueprint

bp = Blueprint('asset', __name__, url_prefix='/pyapi/asset/')


# 内部账号转账记录
@bp.route('plan_transfer_list', methods=['POST', 'GET'])
def customer_plan_transfer_list():
    return Asset().customer_plan_transfer_list()


# 内部账号转账记录-详情
@bp.route('plan_transfer_info', methods=['POST', 'GET'])
def plan_transfer_info():
    return Asset().plan_transfer_info()


# 内部账号转账记录-详情-失败原因添加
@bp.route('plan_transfer_remark', methods=['POST', 'GET'])
def plan_transfer_remark():
    return Asset().plan_transfer_remark()


# 钱包资金流水
@bp.route('wallet_ledger', methods=['POST', 'GET'])
def wallet_flowing():
    return Asset().wallet_flowing()


# 钱包资金流水-编辑说明
@bp.route('wallet_ledger_edit', methods=['POST', 'GET'])
def wallet_flowing_edit():
    return Asset().wallet_flowing_edit()
