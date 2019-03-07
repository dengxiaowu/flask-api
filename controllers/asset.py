import time

from controllers.base import Base
from flask import request
from models.admin import AdminModel
from models.product_plan import ProductPlanModel
from models.product_plan_transfer import ProductPlanTransferModel
from models.transfer_attachments import TransferAttachmentsModel
from models.wallet_flowing import WalletFlowingModel


class Asset(Base):

    def __init__(self):
        super().__init__()
        self.ok = 1
        self.msg = 'ok'

    # 内部账号转账记录
    def customer_plan_transfer_list(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']
        # 资产类型
        asset_type = request.values.get('asset_type', "1")
        if not asset_type.isdigit():
            asset_type = 0
        else:
            asset_type = int(asset_type)
        if asset_type <= 0 or (asset_type not in [1, 2, 3]):
            return self.ret_json(10001, '资产类型')

        # 账号ID
        account_id = request.values.get('account_id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(asset_type)
        if account_id <= 0:
            return self.ret_json(10002, '账号ID错误')

        # 产品方案ID
        plan_id = request.values.get('plan_id', "0")
        if not plan_id.isdigit():
            plan_id = 0
        else:
            plan_id = int(plan_id)

        filter_dic = dict()
        filter_dic['account_id'] = account_id
        if plan_id > 0:
            filter_dic['product_plan_id'] = plan_id
        page = int(request.values.get('page', 1))
        page_size = int(request.values.get('page_size', 20))

        data = ProductPlanTransferModel().get_transfer_list(filter_dic,
                                                            page=page,
                                                            page_size=page_size)

        page_info = self.page_info(data['total'], page, page_size)
        if data['total'] == 0:
            return self.ret_json(self.ok, self.msg, {"list": [], 'page_info': page_info})
        result_list = []
        for item in data['list']:
            item['plan_name'] = Asset.get_plan_name(item["product_plan_id"])
            item['currency'] = item["currency"].upper()
            item['apply_type_name'] = Asset.get_apply_type_name(item["apply_type"])
            item['apply_status_name'] = Asset.get_apply_status_name(item["apply_status"])
            item['carry_interest_status_name'] = Asset.get_carry_interest_status_name(item["carry_interest_status"])
            item['apply_time'] = str(item["apply_time"])
            if item["apply_type"] == 1:
                item['amount'] = "+" + str(float(item['amount']))
            else:
                item['amount'] = "-" + str(float(item['amount']))

            if item["apply_status"] == 1:
                item["finish_time"] = "-"
                item["cumulative_net_value"] = "-"
                item["actual_amount_change"] = "-"
                item["actual_portion_change"] = "-"
                item["accumulated_amount"] = "-"
                item["accumulated_portion"] = "-"
                item["carry_interest"] = "-"
                item["carry_interest_status"] = "-"
                item['carry_interest_status_name'] = "-"
            else:
                item["cumulative_net_value"] = item["cumulative_net_value"] if item["cumulative_net_value"] else ''
                item["actual_amount_change"] = item["actual_amount_change"] if item["actual_amount_change"] else ''
                item["actual_portion_change"] = item["actual_portion_change"] if item["actual_portion_change"] else ''
                item["accumulated_amount"] = item["accumulated_amount"] if item["accumulated_amount"] else ''
                item["accumulated_portion"] = item["accumulated_portion"] if item["accumulated_portion"] else ''
                item["carry_interest"] = item["carry_interest"] if item["carry_interest"] else ''
                item["finish_time"] = str(item["finish_time"])
            result_list.append(item)
            del item
        return self.ret_json(self.ok, self.msg, {"list": result_list, 'page_info': page_info})

    @staticmethod
    def get_plan_name(plan_id):
        plan_info = ProductPlanModel().get_product_plan_info_by_id(plan_id)
        if plan_info:
            return plan_info["plan_name"]
        else:
            return ''

    # 申请类型
    @staticmethod
    def get_apply_type_name(apply_type):
        if apply_type is None or apply_type == 0:
            return '无类型'
        else:
            # 1申购2赎回3分红
            status_map = {'1': '申购', '2': '赎回', '3': '分红'}
            return status_map[str(apply_type)]

    # 申请状态
    @staticmethod
    def get_apply_status_name(apply_status):
        if apply_status is None or apply_status == 0:
            return '无状态'
        else:
            status_map = {'1': '申请中', '2': '成功', '3': '失败'}
            return status_map[str(apply_status)]

    # 分成状态
    @staticmethod
    def get_carry_interest_status_name(carry_interest_status):
        if carry_interest_status is None or carry_interest_status == 0:
            return '无状态'
        else:
            status_map = {'1': '待结算', '2': '已计算'}
            return status_map[str(carry_interest_status)]

    # 转账流水记录详情
    def plan_transfer_info(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        # 流水ID
        t_id = request.values.get('id', "0")
        if not t_id.isdigit():
            t_id = 0
        else:
            t_id = int(t_id)
        if t_id <= 0:
            return self.ret_json(10002, 'ID为空或者错误')

        data = ProductPlanTransferModel().get_transfer_by_id(t_id)

        if data is None:
            return self.ret_json(10003, '流水详情为空')
        else:
            apply = dict()
            apply['id'] = data['id']
            apply['apply_time'] = str(data['apply_time'])
            apply['product_plan_id'] = str(data['product_plan_id'])
            apply['product_plan_name'] = Asset.get_plan_name(data['product_plan_id'])
            apply['currency'] = str(data['currency'])
            apply['apply_type'] = str(data['apply_type'])
            apply['apply_type_name'] = Asset.get_apply_type_name(data["apply_type"])
            if data["apply_type"] == 1:
                apply['amount'] = "+" + str(float(data['amount']))
            else:
                apply['amount'] = "-" + str(float(data['amount']))

            apply['user_name'] = Asset.get_user_name(data['user_id'])
            apply['attachments'] = TransferAttachmentsModel().get_transfer_attachments_by_tran_id(t_id)
            # 根据 申请状态返回转账详情
            trans = dict()
            trans['apply_status'] = data['apply_status']
            trans['apply_status_name'] = Asset.get_apply_status_name(data['apply_status'])
            trans['remark'] = data['remark']
            if data['apply_status'] == 1:
                trans['finish_time'] = '-'
            elif data['apply_status'] == 2:
                trans['finish_time'] = str(data['finish_time'])
            else:
                trans['finish_time'] = str(data['finish_time'])

            result = dict()
            result['apply_info'] = apply
            result['trans_info'] = trans
        return self.ret_json(self.ok, self.msg, result)

    @staticmethod
    def get_plan_name(plan_id):
        plan = ProductPlanModel().get_product_plan_info_by_id(plan_id)
        if plan:
            return plan['plan_name']
        else:
            return ''

    @staticmethod
    def get_user_name(user_id):
        user = AdminModel().get_user_info_by_id(user_id)
        if user:
            return user['name']
        else:
            return ''

    def plan_transfer_remark(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']
        # 流水ID
        t_id = request.values.get('id', "0")
        if not t_id.isdigit():
            t_id = 0
        else:
            t_id = int(t_id)
        if t_id <= 0:
            return self.ret_json(10001, 'ID为空或者错误')

        # remark
        remark = str(request.values.get('remark', ""))
        if remark == '':
            return self.ret_json(10002, 'remark为空')

        data = ProductPlanTransferModel().get_transfer_by_id(t_id)

        if data is None:
            return self.ret_json(10003, '流水详情为空')
        else:
            update = dict()
            update['remark'] = remark
            update['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ret = ProductPlanTransferModel().update_transfer_model(t_id, update)
            if ret is False:
                return self.ret_json(10004, '修改失败')
            else:
                return self.ret_json(self.ok, self.msg)

    # 钱包资金流水
    def wallet_flowing(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']
        # 资产类型
        asset_type = request.values.get('asset_type', "1")
        if not asset_type.isdigit():
            asset_type = 0
        else:
            asset_type = int(asset_type)
        if asset_type <= 0 or (asset_type not in [1, 2, 3]):
            return self.ret_json(10001, '资产类型')

        # 账号ID
        account_id = request.values.get('account_id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(account_id)
        if account_id <= 0:
            return self.ret_json(10002, '账号ID错误')

        page = int(request.values.get('page', 1))
        page_size = int(request.values.get('page_size', 20))

        data = WalletFlowingModel().get_flow_list(account_id=account_id,
                                                  page=page,
                                                  page_size=page_size)

        page_info = self.page_info(data['total'], page, page_size)
        if data['total'] == 0:
            return self.ret_json(self.ok, self.msg, {"list": [], 'page_info': page_info})

        result_list = data['list']
        for item in result_list:
            item['amount'] = str(float(item['amount']))
            item['ctime'] = str(item['ctime'])

        return self.ret_json(self.ok, self.msg, {"list": result_list, "page_info": page_info})

    # 流水说明编辑
    def wallet_flowing_edit(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        w_id = request.values.get('id', "")
        if not w_id.isdigit():
            w_id = 0
        else:
            w_id = int(w_id)
        if w_id <= 0:
            return self.ret_json(10001, 'id为空或者错误')

        # 说明
        remark = str(request.values.get('remark', ''))
        if remark == '':
            return self.ret_json(10002, '说明为空')
        params = dict()
        params['remark'] = remark
        params['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        params['user_id'] = user_id
        result = WalletFlowingModel().update_flow_remark(w_id, params)

        if result is False:
            return self.ret_json(1003, '更新错误')
        else:
            return self.ret_json(self.ok, self.msg)
