from controllers.base import Base
from flask import request
from models.account import CustomerAccountModel
from models.admin import AdminModel
from models.product_plan import ProductPlanModel


class Account(Base):

    def __init__(self):
        super().__init__()

    # 添加
    def account_add(self):
        params = request.values

        params_isvalid = self.check_account_params_isvalid(params)
        if params_isvalid is not True:
            return params_isvalid
        else:
            # 操作管理员ID
            user_id = self.check_token()['user_id']

        customer_id = params.get('customer_id', "0")
        # 账号类型 1.数字货币 2.股票 3.商品期货
        account_type = params.get('account_type', "0")
        # 交易所  1 :okex  2:bitmex
        exchange = params.get('exchange', "0")
        account_name = params.get('account_name', '')
        api_key = params.get('api_key', '')
        secret_key = params.get('secret_key', '')
        # bitmex 没有passphrase
        pass_phrase = params.get('pass_phrase', '')
        customer_account = params.get('customer_account', '')
        customer_password = params.get('customer_password', '')
        remark = params.get('remark', '')

        params_dic = {'user_id': user_id, 'customer_id': customer_id, 'account_type': account_type,
                      'exchange': exchange, 'account_name': account_name, 'api_key': api_key,
                      'secret_key': secret_key, 'pass_phrase': pass_phrase, 'customer_account': customer_account,
                      'customer_password': customer_password, 'remark': remark}

        account_model = CustomerAccountModel()
        account_info = account_model.get_info_by_params(customer_id, account_name, api_key, secret_key)
        if account_info:
            if account_info.get('status') == 0:
                return self.ret_json(10001, '不能添加相同账号')
            else:
                params_dic['status'] = 0
                result = account_model.account_update(account_id=account_info['id'], datas=params_dic)
        else:
            result = account_model.account_add(params_dic)

        return self.ret_json(1, 'ok', {'id': str(result)})

    def check_account_params_isvalid(self, params):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']
        customer_id = params.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)
        # 账号类型 1.数字货币 2.股票 3.商品期货
        account_type = params.get('account_type', "0")
        if not account_type.isdigit():
            account_type = 1
        else:
            account_type = int(account_type)
        # 交易所  1 :okex  2:bitmex
        exchange = params.get('exchange', "0")
        if not exchange.isdigit():
            exchange = 1
        else:
            exchange = int(exchange)
        account_name = params.get('account_name', '')
        api_key = params.get('api_key', '')
        secret_key = params.get('secret_key', '')
        # bitmex 没有passphrase
        pass_phrase = params.get('pass_phrase', '')

        if customer_id <= 0:
            return self.ret_json(10001, '客户id错误')
        if 0 == user_id:
            return self.ret_json(10002, '管理人id不能为空')
        if not AdminModel().check_user_isvalid('', uid=user_id):
            return self.ret_json(-1, '管理人id不可用')
        if account_type not in [1, 2, 3]:
            return self.ret_json(10003, '账号类型异常')
        if 0 == exchange or exchange not in [1, 2]:
            return self.ret_json(10004, '请选择交易所')
        if 0 == len(account_name):
            return self.ret_json(10005, '请填写账号名称')
        if 0 == len(api_key):
            return self.ret_json(10006, '请填写api key')
        if 0 == len(secret_key):
            return self.ret_json(10007, '请填写secret key')
        if 0 == len(pass_phrase) and exchange != 2:
            return self.ret_json(10008, '请填写pass phrase')

        return True

    def account_info(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        account_id = request.values.get('account_id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(account_id)

        if account_id <= 0:
            return self.ret_json(10001, 'id错误')

        model = CustomerAccountModel()
        account_info = model.get_info_by_account_id(account_id)
        if isinstance(account_info, dict):
            for key in ['ctime', 'mtime', 'status']:
                del account_info[key]

            for key, value in account_info.items():
                account_info[key] = str(value)
            return self.ret_json(1, 'ok', account_info)
        else:
            return self.ret_json(1, 'ok', {})

    def account_del(self):

        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info
        else:
            # 操作管理员ID
            user_id = token_info['user_id']

        account_id = request.values.get('id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(account_id)

        if account_id <= 0:
            return self.ret_json(10001, '账户id异常')

        # 如果该账号已经成为客户某个产品所添加的账号时，该账号不能够删除，删除按钮直接隐藏
        plans = ProductPlanModel().get_product_plan_info_by_aid(account_id)
        if plans:
            return self.ret_json(10002, '该账号涉及方案，不能删除')

        model = CustomerAccountModel()
        model.account_del(account_id, user_id)

        return self.ret_json(1, 'ok', {})

    # 更新
    def account_update(self):
        params = request.values
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info
        else:
            # 操作管理员ID
            user_id = token_info['user_id']

        account_id = request.values.get('id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(account_id)
        if account_id <= 0:
            return self.ret_json(10001, '账户id异常')

        account_model = CustomerAccountModel()
        account_info = account_model.get_info_by_account_id(account_id)
        if not isinstance(account_info, dict):
            return self.ret_json(10002, '账号不存在或者被删除')

        params_dic = {'user_id': user_id}

        customer_account = params.get('customer_account', '')
        customer_password = params.get('customer_password', '')
        remark = params.get('remark', '')
        if customer_account:
            params_dic['customer_account'] = customer_account
        if customer_password:
            params_dic['customer_password'] = customer_password
        if remark:
            params_dic['remark'] = remark

        account_model.account_update(account_id=account_id, datas=params_dic)

        return self.ret_json(1, 'ok', {})

    # 客户的账号详情列表
    def account_list(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info
        else:
            # 操作管理员ID
            user_id = token_info['user_id']

        customer_id = request.values.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)

        if customer_id <= 0:
            return self.ret_json(10001, '客户id异常')

        account_model = CustomerAccountModel()
        account_list = account_model.get_info_by_customer_id(customer_id)

        if account_list is False:
            return self.ret_json(1, 'ok', [])
        else:
            for item in account_list:
                item['account_type_name'] = Account.get_account_type_name(item['account_type'])
                item['exchange_name'] = Account.get_exchange_name(item['exchange'])
            return self.ret_json(1, 'ok', account_list)

    @staticmethod
    def get_account_type_name(account_type):
        type_map = {
            '1': '数字货币',
            '2': '股票',
            '3': '商品期货',
        }
        return type_map[str(account_type)]

    @staticmethod
    def get_exchange_name(exchange):
        status_map = {
            '1': 'OKEX',
            '2': 'BITMEX',
        }
        return status_map[str(exchange)]
