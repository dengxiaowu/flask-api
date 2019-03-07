import json
import time

from controllers.base import Base
from flask import request
from library.logger import Logger
from models.account import CustomerAccountModel
from models.customer import CustomerModel
from models.product import ProductModel
from models.product_plan import ProductPlanModel
from models.product_plan_attachments import ProductPlanAttachModel


class ProductPlan(Base):

    def __init__(self):
        super().__init__()

    def write_log(self, content, level='info'):
        logger = Logger()
        logger.name = 'flask_test'
        logger.path = '/home/dengxiaowu/python/mini_flask/'
        logger.logger = True
        logger.output_log(content, level=level)
        logger.removestreamhandler()
        logger.removefilehandler()

    # 添加
    def product_plan_add(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        customer_id = request.values.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)
        if customer_id <= 0:
            return self.ret_json(10001, '客户ID为空')

        account_id = request.values.get('account_id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(account_id)
        if account_id <= 0:
            return self.ret_json(10002, '账号ID为空')

        product_id = request.values.get('product_id', "0")
        if not product_id.isdigit():
            product_id = 0
        else:
            product_id = int(product_id)
        if product_id <= 0:
            return self.ret_json(10003, '产品ID为空')

        asset_type = request.values.get('asset_type', "0")
        if not asset_type.isdigit():
            asset_type = 0
        else:
            asset_type = int(asset_type)
        if asset_type <= 0:
            return self.ret_json(10004, '资产类型为空')
        if asset_type not in [1, 2]:
            return self.ret_json(2, '资产类型错误')

        currency = str(request.values.get('currency', '')).upper()
        if currency == '' or currency not in ['BTC', 'ETH', 'USDT', 'EOS']:
            return self.ret_json(10005, '币种错误或者为空')

        amount = request.values.get('amount', "0.0")
        if not self.isfloat(amount):
            amount = 0
        else:
            amount = float(amount)
        if amount <= 0:
            return self.ret_json(10006, '币种数量错误或者为空')

        start_time = str(request.values.get('start_time', ''))
        if start_time == '':
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        lockup_ends = request.values.get('lockup_ends', "0")
        if not lockup_ends.isdigit():
            lockup_ends = 0
        else:
            lockup_ends = int(lockup_ends)

        if lockup_ends <= 0:
            return self.ret_json(10007, '封闭期错误或者为空')

        open_time = str(request.values.get('open_time', ''))
        if open_time == '':
            return self.ret_json(10008, '开放期为空')

        accounting_currency = str(request.values.get('accounting_currency', '')).upper()
        if accounting_currency == '':
            return self.ret_json(10009, '结算币种错误或者为空')

        management_fee = request.values.get('management_fee', '')
        if management_fee == '':
            return self.ret_json(10010, '管理费为空')

        carry_interest = request.values.get('carry_interest', '')
        if carry_interest == '':
            return self.ret_json(10011, '收益分成为空')

        principal_guarantee = request.values.get('principal_guarantee', "0")
        if not principal_guarantee.isdigit():
            principal_guarantee = 0
        else:
            principal_guarantee = int(principal_guarantee)
        if principal_guarantee not in [0, 1]:
            return self.ret_json(10012, '保底协议类型错误')

        remark = request.values.get('remark', '')

        # 附件 json
        attachments = request.values.get('attachments', '')
        list_att = {}
        if attachments:
            list_att = json.loads(attachments)

        insert_data = dict()
        insert_data['customer_id'] = customer_id
        insert_data['asset_type'] = asset_type
        insert_data['product_id'] = product_id
        insert_data['account_id'] = account_id
        insert_data['plan_name'] = ProductPlan.get_plan_name(product_id, customer_id, account_id)
        insert_data['currency'] = currency
        insert_data['amount'] = amount
        insert_data['start_time'] = start_time
        insert_data['lockup_ends'] = lockup_ends
        insert_data['accounting_currency'] = accounting_currency
        insert_data['management_fee'] = management_fee
        insert_data['carry_interest'] = carry_interest
        insert_data['principal_guarantee'] = principal_guarantee
        insert_data['remark'] = remark
        insert_data['user_id'] = user_id
        insert_id = ProductPlanModel().add_product_plan_model(insert_data)
        if insert_id is False:
            return self.ret_json(10013, '添加失败')
        else:
            # 添加附件
            if len(list_att) > 0:
                for url in list_att:
                    a_data = dict()
                    a_data['product_plan_id'] = insert_id
                    a_data['url'] = url
                    a_data['remark'] = remark
                    a_data['user_id'] = user_id
                    ProductPlanAttachModel().add_attachments_model(a_data)
                    a_data.clear()

            return self.ret_json(1, 'ok', {'plan_id': insert_id})

    @staticmethod
    def get_plan_name(product_id, customer_id, account_id):
        # 判断是否存在账号购买过这个产品
        p_list = ProductPlanModel().get_product_plan_by_params(
            params={"customer_id": customer_id, "account_id": account_id, "product_id": product_id})
        if p_list is None:
            num = 1
        else:
            num = int(len(p_list)) + 1
        product = ProductModel().get_product_info_by_id(product_id)
        customer = CustomerModel().get_info_by_id('', '', '', uid=customer_id)
        if product and customer:
            return product['product_name'] + '-' + customer['name'] + '-' + str(num) + '期'
        else:
            return ''

    # 列表=分页
    def product_plan_list(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        customer_id = request.values.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)
        if customer_id <= 0:
            return self.ret_json(10001, '客户ID为空')

        # 获取客户的投资状态
        customer_info = CustomerModel().get_info_by_id('', '', '', customer_id)
        # 客户投资状态1：接触中 2：暂停搁置 3：投资中
        customer = dict()
        if customer_info:
            customer['customer_id'] = customer_id
            customer['invest_status'] = customer_info['invest_status']

        page = int(request.values.get('page', 1))
        page_size = int(request.values.get('page_size', 20))

        filter_dic = {"customer_id": customer_id}
        data = ProductPlanModel().get_plan_list(filter_dic, page, page_size)

        page_info = self.page_info(data['total'], page, page_size)
        if data['total'] == 0:
            return self.ret_json(self.ok, self.msg, {"list": [], "customer": customer, 'page_info': page_info})
        result_list = []
        for item in data['list']:
            item["asset_type_name"] = ProductPlan.get_asset_name(item['asset_type'])
            item["amount"] = '%.4f' % (float(item['amount']))
            item["balance"] = '%.4f' % (float(item['balance']))
            item["cumulative_net_value"] = ProductPlan.cumulative_net_value()
            result_list.append(item)
            del item

        return self.ret_json(self.ok, self.msg, {"list": result_list, "customer": customer, 'page_info': page_info})

    @staticmethod
    def get_asset_name(asset_type):
        data = {
            "1": "数字货币",
            "2": "股票"
        }
        return data[str(asset_type)]

    @staticmethod
    def cumulative_net_value():
        return '1.0000'

    # 方案详情
    def product_plan_info(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        plan_id = request.values.get('id', '0')
        if not plan_id.isdigit():
            plan_id = 0
        else:
            plan_id = int(plan_id)
        if plan_id <= 0:
            return self.ret_json(10001, 'ID为空')

        # 是否存在
        product_plan_info = ProductPlanModel().get_product_plan_info_by_id(plan_id)
        if product_plan_info is None:
            return self.ret_json(10002, '该产品方案不存在')
        else:
            result = dict()
            result['plan_id'] = str(plan_id)
            result['asset_type'] = product_plan_info['asset_type']
            result['asset_type_name'] = ProductPlan.get_asset_name(product_plan_info['asset_type'])
            result["product_id"] = product_plan_info['product_id']
            product = ProductModel().get_product_info_by_id(product_plan_info['product_id'])
            result["product_name"] = product['product_name'] if product else ''
            result["account_id"] = product_plan_info['account_id']
            result["account_name"] = ProductPlan.get_account_name(product_plan_info['customer_id'],
                                                                  product_plan_info['account_id'])
            result["start_time"] = str(product_plan_info['start_time'])
            result["currency"] = str(product_plan_info['currency'])
            result["lockup_ends"] = str(product_plan_info['lockup_ends']) + '个月'
            result["management_fee"] = str(product_plan_info['management_fee']) if product_plan_info[
                'management_fee'] else '暂无'
            result['carry_interest'] = str(product_plan_info['carry_interest'])
            result['principal_guarantee'] = ProductPlan.get_principal_guarantee(
                product_plan_info['principal_guarantee'])
            result['remark'] = str(product_plan_info['remark'])
            result['attachments'] = ProductPlan.get_attachments(plan_id)

            return self.ret_json(self.ok, self.msg, result)

    @staticmethod
    def get_account_name(customer_id, account_id):
        customer = CustomerModel().get_info_by_id('', '', '', uid=customer_id)
        account = CustomerAccountModel().get_info_by_account_id(account_id)

        if customer and account:
            return customer['name'] + '-' + account['account_name']
        else:
            return ''

    @staticmethod
    def get_attachments(plan_id):

        att_list = ProductPlanAttachModel().get_attachments_by_plan_id(plan_id)
        return att_list

    @staticmethod
    def get_principal_guarantee(principal_guarantee):
        data = {
            '0': '否',
            '1': '是'
        }
        return data[str(principal_guarantee)]

    # 删除方案
    def product_plan_del(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        plan_id = request.values.get('id', '0')
        if not plan_id.isdigit():
            plan_id = 0
        else:
            plan_id = int(plan_id)
        if plan_id <= 0:
            return self.ret_json(10001, 'ID为空')

        # 是否存在
        product_plan_info = ProductPlanModel().get_product_plan_info_by_id(plan_id)
        if product_plan_info is None:
            return self.ret_json(10002, '该产品方案不存在')
        else:
            update_data = dict()
            update_data['status'] = 1
            update_data['user_id'] = user_id
            update_data['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ret = ProductPlanModel().del_product_plan_model(plan_id, update_data)
            if ret is False:
                return self.ret_json(10003, '删除错误')
            return self.ret_json(1, 'ok')

    # 更新
    def product_plan_update(self):
        pass

    # 方案收益统计
    def product_plan_earnings(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        plan_id = request.values.get('id', '0')
        if not plan_id.isdigit():
            plan_id = 0
        else:
            plan_id = int(plan_id)
        if plan_id <= 0:
            return self.ret_json(10001, 'ID为空')

        # 是否存在
        product_plan_info = ProductPlanModel().get_product_plan_info_by_id(plan_id)
        if product_plan_info is None:
            return self.ret_json(10002, '该产品方案不存在')
        else:
            result = dict()
            result['plan_id'] = str(plan_id)
            result['amount'] = '%.4f' % float(product_plan_info['amount'])
            result['balance'] = '%.4f' % float(product_plan_info['balance'])
            result["cumulative_net_value"] = ProductPlan.cumulative_net_value()
            result['value_list'] = []

            return self.ret_json(self.ok, self.msg, result)

    # 客户账号的方案列表-下拉
    def get_account_plan_list(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        customer_id = request.values.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)
        if customer_id <= 0:
            return self.ret_json(10001, '客户ID为空')

        account_id = request.values.get('account_id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(account_id)
        if account_id <= 0:
            return self.ret_json(10002, '账号ID为空')

        product_plan_list = ProductPlanModel().get_product_plan_list_by_cid_and_aid(customer_id, account_id)
        if product_plan_list is None:
            return self.ret_json(1, 'ok', [])
        else:
            return self.ret_json(1, 'ok', product_plan_list)
