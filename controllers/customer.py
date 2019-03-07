import json
import re

from controllers.base import Base
from flask import request
from models.account import CustomerAccountModel
from models.account_balance import CustomerAccountBalanceModel
from models.admin import AdminModel
from models.customer import CustomerModel
from models.customer_invest import CustomerInvestModel
from models.product import ProductModel
from models.product_plan import ProductPlanModel
from models.product_plan_transfer import ProductPlanTransferModel
from models.transfer_attachments import TransferAttachmentsModel


class Customer(Base):

    def __init__(self):
        super().__init__()

    # 添加
    def customer_add(self):
        params_isvalid = self.check_customer_params_isvalid()
        if params_isvalid != 1:
            return params_isvalid
        else:
            # 操作管理员ID
            user_id = self.check_token()['user_id']

        # 企业1 个人2
        customer_type = request.values.get('customer_type', '')
        # 用户名, 企业名称
        name = request.values.get('name', '')
        mobile = request.values.get('mobile', '')
        # 职位
        title = request.values.get('title', '')
        # 工作单位
        company = request.values.get('company', '')
        # 身份证
        id_card = request.values.get('id_card', '')
        # 微信
        wechat = request.values.get('wechat', '')
        email = request.values.get('email', '')
        address = request.values.get('address', '')
        # 纳税号
        tax_number = request.values.get('tax_number', '')
        # 法人代表
        legal_representative = request.values.get('legal_representative', '')
        # 企业联系人
        business_contact = request.values.get('business_contact', '')
        # 备注
        remark = request.values.get('remark', '')
        # '客户投资状态1：接触中 2：暂停搁置 3：投资中',
        invest_status = request.values.get('invest_status', '')
        # 搁置说明
        invest_remark = request.values.get('invest_remark', '')
        # 跟进人
        salesrep = request.values.get('salesrep', '')

        customer_dic = {'customer_type': customer_type,
                        'name': name,
                        'mobile': mobile,
                        'title': title,
                        'company': company,
                        'id_card': id_card,
                        'wechat': wechat,
                        'email': email,
                        'address': address,
                        'tax_number': tax_number,
                        'legal_representative': legal_representative,
                        'business_contact': business_contact,
                        'remark': remark,
                        'invest_status': invest_status,
                        'invest_remark': invest_remark,
                        'salesrep': salesrep,
                        'user_id': user_id
                        }
        model = CustomerModel()
        customer_info = model.get_info_by_id(customer_type, mobile, name)
        if customer_info:
            if customer_info.get('status') == 0 and customer_type == '1':
                return self.ret_json(10001, '该公司已经存在')
            elif customer_info.get('status') == 0 and customer_type == '2':
                return self.ret_json(10002, '该手机号已经存在')
            else:
                result = model.update_by_id(uid=customer_info['uid'], datas=customer_dic)
        else:
            result = model.add_customer_model(customer_dic)
            if len(invest_remark) > 0:
                CustomerInvestModel().add({'customer_id': result, 'invest_status': invest_status,
                                           'invest_remark': invest_remark, 'user_id': user_id})

        return self.ret_json(1, 'ok', {'id': str(result)})

    def check_customer_params_isvalid(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        # 管理员
        user_id = token_info['user_id']
        # 企业1 个人2 必填
        customer_type = request.values.get('customer_type', "1")
        if not customer_type.isdigit():
            customer_type = 1
        customer_type = int(customer_type)
        # 用户名 必填
        name = request.values.get('name', '')
        # 必填
        mobile = request.values.get('mobile', '')
        # 工作单位
        company = request.values.get('company', '')
        address = request.values.get('address', '')
        # 企业联系人
        business_contact = request.values.get('business_contact', '')
        # '客户投资状态1：接触中 2：暂停搁置 3：投资中', 必填
        invest_status = request.values.get('invest_status', "1")
        if not invest_status.isdigit():
            invest_status = 1
        invest_status = int(invest_status)
        # 搁置说明
        invest_remark = request.values.get('invest_remark', '')
        # 跟进人 必填
        salesrep = request.values.get('salesrep', "0")
        if not salesrep.isdigit():
            salesrep = 1
        else:
            salesrep = int(salesrep)

        if customer_type <= 0:
            return self.ret_json(10001, '客户类型错误')

        if customer_type not in [1, 2]:
            return self.ret_json(10010, '请选择客户类型')
        if 0 == len(str(user_id)):
            return self.ret_json(10002, '管理人id不能为空')
        if not AdminModel().check_user_isvalid('', uid=user_id):
            return self.ret_json(10003, '管理人id不可用')
        # 企业
        if customer_type == 1:
            if 0 == len(name):
                return self.ret_json(10004, '请填写企业名称')
            if 0 == len(address):
                return self.ret_json(10005, '请填写企业地址')
            if 0 == len(business_contact):
                return self.ret_json(10006, '请填写企业联系人')
        elif customer_type == 2:
            if 0 == len(name):
                return self.ret_json(10007, '请填写客户名称')

        if 0 == len(mobile):
            return self.ret_json(10008, '请填写联系人手机号')
        if re.match(r'^\d{11}$', mobile) is None:
            return self.ret_json(10009, '手机号码异常')
        if invest_status <= 0:
            return self.ret_json(10010, '请选择投资状态')
        if invest_status not in [1, 2, 3, 4]:
            return self.ret_json(10011, '投资状态异常')
        if invest_status == 2 and len(invest_remark) == 0:
            return self.ret_json(10012, '请填写搁置说明')
        if salesrep <= 0:
            return self.ret_json(10013, '请填写跟进人')

        return 1

    # 跟进人列表
    def salesrep_list(self):
        salesr_list = [
            {'id': '1', 'salesrep': '王辉'},
            {'id': '2', 'salesrep': '王博士'},
        ]
        return self.ret_json(1, 'ok', salesr_list)

    # 客户详情(客户基本信息)
    def customer_info(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        model = CustomerModel()
        customer_id = request.values.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)
        if customer_id <= 0:
            return self.ret_json(10001, '客户id为空')
        if not model.check_customer_isvalid('', '', '', uid=customer_id):
            return self.ret_json(10002, '无效的客户id')

        customer_info = model.get_info_by_id('', '', '', uid=customer_id)
        for key in ['ctime', 'mtime']:
            del customer_info[key]

        for key, value in customer_info.items():
            customer_info[key] = str(value)

        customer_info['customer_type_name'] = Customer.get_customer_type_name(customer_info['customer_type'])
        customer_info['invest_status_name'] = Customer.get_invest_status_name(customer_info['invest_status'])
        customer_info['salesrep_name'] = Customer.get_salesrep_name(customer_info['salesrep'])
        customer_info['invest_remark'] = []
        if customer_info['invest_status'] == "2":
            customer_info['invest_remark'] = CustomerInvestModel().get_invest_remark_list(customer_id)

        return self.ret_json(1, 'ok', customer_info)

    # 跟进人列表
    @staticmethod
    def get_salesrep_name(salesrep):
        salesr_list = {
            '1': '王辉',
            '2': '王博士',
        }
        return salesr_list[str(salesrep)]

    def customer_del(self):
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
            return self.ret_json(10001, '客户id为空')

        model = CustomerModel()
        usr_info = model.get_info_by_id('', '', '', customer_id)
        if not usr_info:
            return self.ret_json(10002, '不存在该用户')
        if usr_info['invest_status'] == 3:
            return self.ret_json(10003, '投资中的用户无法删除')

        model.del_by_id(customer_id, user_id)
        return self.ret_json(1, 'ok')

    # 更新
    def customer_update(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info
        # 管理员
        user_id = token_info['user_id']

        customer_id = request.values.get('customer_id', '0')
        if not customer_id.isdigit():
            customer_id = 0
        customer_id = int(customer_id)
        if customer_id <= 0:
            return self.ret_json(10004, '客户ID为空')
        # 企业1 个人2 必填
        customer_type = request.values.get('customer_type', "0")
        if not customer_type.isdigit():
            customer_type = 1
        customer_type = int(customer_type)
        if customer_type <= 0:
            return self.ret_json(10001, '请选择客户类型')
        if customer_type not in [1, 2]:
            return self.ret_json(10002, '客户类型错误')

        business_contact = ''
        # 个人客户
        if customer_type == 2:
            # 用户名 必填
            name = str(request.values.get('name', ''))
            if name == '':
                return self.ret_json(10003, '请填写客户名称')
        else:
            # 必填
            # 公司名字
            name = str(request.values.get('name', ''))
            if name == '':
                return self.ret_json(10003, '请填写公司名称')
            # 企业地址
            address = str(request.values.get('address', ''))
            # 企业联系人
            business_contact = str(request.values.get('business_contact', ''))
            if 0 == len(address):
                return self.ret_json(10005, '请填写企业地址')
            if 0 == len(business_contact):
                return self.ret_json(10006, '请填写企业联系人')

        # 公共部分
        # 手机
        mobile = str(request.values.get('mobile', ''))
        if 0 == len(mobile):
            return self.ret_json(10008, '请填写联系人手机号')
        if re.match(r'^\d{11}$', mobile) is None:
            return self.ret_json(10009, '手机号码异常')
        # '客户投资状态1：接触中 2：暂停搁置 3：投资中', 必填
        invest_status = request.values.get('invest_status', "1")
        if not invest_status.isdigit():
            invest_status = 1
        invest_status = int(invest_status)
        # 搁置说明
        invest_remark = request.values.get('invest_remark', '')
        if invest_status <= 0:
            return self.ret_json(10010, '请选择投资状态')
        if invest_status not in [1, 2, 3, 4]:
            return self.ret_json(10011, '投资状态异常')
        if invest_status == 2 and len(invest_remark) == 0:
            return self.ret_json(10012, '请填写搁置说明')
        # 跟进人 必填
        salesrep = request.values.get('salesrep', "0")
        if not salesrep.isdigit():
            salesrep = 1
        else:
            salesrep = int(salesrep)
        if salesrep <= 0:
            return self.ret_json(10013, '请填写跟进人')

        # 个人
        # 职位
        title = request.values.get('title', '')
        # 工作单位
        company = request.values.get('company', '')

        # 企业
        # 纳税号
        tax_number = request.values.get('tax_number', '')
        # 法人代表
        legal_representative = request.values.get('legal_representative', '')

        # 公共部分
        # 身份证
        id_card = request.values.get('id_card', '')
        # 微信
        wechat = request.values.get('wechat', '')
        email = request.values.get('email', '')
        address = request.values.get('address', '')
        # 备注
        remark = request.values.get('remark', '')

        model = CustomerModel()

        customer_info = model.get_info_by_id('', '', '', customer_id)
        # 客户投资状态1：接触中 2：暂停搁置 3：投资中
        if customer_info['customer_type'] != customer_type:
            return self.ret_json(10014, '客户类型不能改变')
        if customer_info['invest_status'] == 3 and invest_status != 3:
            return self.ret_json(10015, '投资中的状态不能改成别的状态')

        # 企业
        if customer_type == 1:
            ret = model.update_by_id(customer_id, {
                'customer_type': customer_type,
                'name': name,  # 企业名字
                'tax_number': tax_number,  # 企业纳税人识别号
                'legal_representative': legal_representative,  # 法人代表
                'id_card': id_card,  # 法人身份证号
                'address': address,  # 企业地址
                'business_contact': business_contact,  # 企业联系人
                'mobile': mobile,  # 联系人手机号
                'wechat': wechat,  # 微信
                'email': email,  # 电子邮箱
                'invest_status': invest_status,  # 投资状态
                'remark': remark,  # 备注
                'salesrep': salesrep,  # 跟进人
                'user_id': user_id
            })
        else:
            ret = model.update_by_id(customer_id, {
                'customer_type': customer_type,
                'name': name,  # 名字
                'mobile': mobile,  # 手机号
                'title': title,  # 职位
                'company': company,  # 公司
                'id_card': id_card,  # 身份证号
                'wechat': wechat,  # 微信
                'email': email,  # 电子邮箱
                'address': address,  # 地址
                'remark': remark,  # 备注
                'invest_status': invest_status,  # 投资状态
                'salesrep': salesrep,  # 跟进人
                'user_id': user_id
            })

        if ret is False:
            return self.ret_json(10016, '更新失败')
        if len(invest_remark) > 0:
            CustomerInvestModel().add({'customer_id': customer_id, 'invest_status': invest_status,
                                       'invest_remark': invest_remark, 'user_id': user_id})

        return self.ret_json(1, 'ok', {})

    # 客户列表
    def customer_list(self):
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        page = int(request.values.get('page', 1))
        page_size = int(request.values.get('page_size', 10))
        # '客户投资状态1：接触中 2：暂停搁置 3：投资中',
        invest_status = request.values.get('status', "0")
        if not invest_status.isdigit():
            invest_status = 0
        else:
            invest_status = int(invest_status)

        customer_type = request.values.get('type', "0")
        if not customer_type.isdigit():
            customer_type = 0
        else:
            customer_type = int(customer_type)

        if page == 0:
            return self.ret_json(10001, 'page异常')
        if page_size == 0:
            return self.ret_json(10002, 'page_size异常')

        filters_dic = {'status': 0}
        if invest_status != 0:
            filters_dic['invest_status'] = invest_status
        if customer_type != 0:
            filters_dic['customer_type'] = customer_type

        model = CustomerModel()

        customer_list = []
        total_count = len(model.get_info_total_by_filters(filters_dic))
        if total_count > 0:
            customer_list = model.get_info_list(page, page_size, filters=filters_dic)
            customer_count = len(customer_list)
            for customer in customer_list:
                customer['list_id'] = customer_count
                customer['customer_id'] = customer['id']
                if customer['customer_type'] == 1:
                    customer['name'] = customer['business_contact']
                customer['invest_status_name'] = Customer.get_invest_status_name(customer['invest_status'])
                customer['customer_type_name'] = Customer.get_customer_type_name(customer['customer_type'])
                customer['salesrep_name'] = Customer.get_salesrep_name(customer['salesrep'])
                del customer['id']
                del customer['business_contact']
                customer_count = customer_count - 1

        page_info = self.page_info(total_count, page, page_size)
        return self.ret_json(1, 'ok', {'list': customer_list, 'page_info': page_info})

    @staticmethod
    def get_customer_type_name(customer_type):
        type_map = {
            '1': '企业客户',
            '2': '个人客户',
        }
        return type_map[str(customer_type)]

    @staticmethod
    def get_invest_status_name(invest_status):
        status_map = {
            '1': '接触中',
            '2': '暂停搁置',
            '3': '投资中',
        }
        return status_map[str(invest_status)]

    # 客户账号列表
    def customer_account_list(self):

        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        # 客户ID
        customer_id = request.values.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)

        if customer_id <= 0:
            return self.ret_json(10001, '客户ID为空')
        data = list()
        accounts = CustomerAccountModel().get_info_by_customer_id(customer_id)
        if accounts:
            for item in accounts:
                data.append({"account_id": str(item['id']), "account_name": str(item['account_name'])})

        return self.ret_json(self.ok, self.msg, data)

    # 客户资产账号详情
    def customer_account_assets(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']
        account_id = request.values.get('account_id', "0")
        if not account_id.isdigit():
            account_id = 0
        else:
            account_id = int(account_id)
        if account_id <= 0:
            return self.ret_json(10001, '账号ID错误')

        data = dict()
        data['input_assets'] = []
        data['allocated_assets'] = []
        data['unallocated_assets'] = []

        # 累计转入资金
        inputs = CustomerAccountBalanceModel().account_balance_info(account_id)
        if inputs is None:
            return self.ret_json(1, 'ok')
        else:
            for item in inputs:
                data['input_assets'].append(
                    {"currency": item['currency'], "amount": float(item['amount']), "frozen": float(item['frozen'])})

        # 已经分配资金产品方案列表
        data['allocated_assets'] = []
        allocated_assets = ProductPlanModel().get_product_plan_info_by_aid(account_id)
        if allocated_assets:
            for asset in allocated_assets:
                asset['plan_id'] = str(asset['id'])
                asset['amount'] = str(float(asset['amount']))
                asset['product_plan_name'] = str(asset['plan_name'])
                asset['balance'] = '%.4f' % (float(asset['balance']))
                asset['frozen'] = '%.4f' % (float(asset['frozen']))
                del asset['id']
                data['allocated_assets'].append(asset)

        # 获取账号的各个币种的累计分配资金
        had_assets = []
        for currency_info in inputs:
            had_asset = ProductPlanModel().get_product_plan_info_by_aid_and_currency(account_id,
                                                                                     currency_info['currency'])
            if had_asset is None or had_asset['currency'] is None:
                had_assets.append({"currency": currency_info['currency'], "amount": float(0)})
            else:
                had_assets.append({"currency": currency_info['currency'], "amount": float(had_asset['amount'])})

        if had_assets:
            data['unallocated_assets'] = Customer.handle_assets(data['input_assets'], had_assets)
            # 累计转入
            for all in data['input_assets']:
                all['amount'] = '%.4f' % float(all['amount'])
                all['frozen'] = '%.4f' % float(all['frozen'])
            # 已经分配
            for allocated in data['allocated_assets']:
                allocated['amount'] = '%.4f' % float(allocated['amount'])
                allocated['frozen'] = '%.4f' % float(allocated['frozen'])
        else:
            # 没有已经分配过的资金
            # 累计转入
            for all in data['input_assets']:
                all['amount'] = '%.4f' % float(all['amount'])
                all['frozen'] = '%.4f' % float(all['frozen'])

            data['unallocated_assets'] = data['input_assets']

        return self.ret_json(self.ok, self.msg, data=data)

    @staticmethod
    def handle_assets(all_assets, had_assets):
        unallocated_assets = []
        for item in all_assets:
            for had in had_assets:
                if item['currency'] == had['currency']:
                    unallocated_assets.append(
                        {"currency": had["currency"],
                         "amount": '%.4f' % (float(item["amount"]) - float(item["frozen"]) - float(had['amount'])),
                         "frozen": '%.4f' % float(item["frozen"])
                         })

        return unallocated_assets

    @staticmethod
    def get_product_plan_name(customer_id, product_id):
        customer_info = CustomerModel().get_info_by_id('', '', '', uid=customer_id)
        product_info = ProductModel().get_product_info_by_id(product_id)
        if customer_info and product_info:
            return customer_info['name'] + '-' + product_info['product_name']
        else:
            return ''

    # 资金划转=1:申购,2:赎回,:3分红
    def assets_change(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']
        # 客户ID
        customer_id = request.values.get('customer_id', "0")
        if not customer_id.isdigit():
            customer_id = 0
        else:
            customer_id = int(customer_id)
        if customer_id <= 0:
            return self.ret_json(10001, '客户ID错误')
        # 资产类型
        asset_type = request.values.get('asset_type', "1")
        if not asset_type.isdigit():
            asset_type = 1
        else:
            asset_type = int(asset_type)
        if asset_type <= 0 or (asset_type not in [1, 2, 3]):
            return self.ret_json(10002, '资产类型')

        # 申请类型：1申购2赎回3分红
        apply_type = request.values.get('apply_type', "1")
        if not apply_type.isdigit():
            apply_type = 1
        else:
            apply_type = int(apply_type)
        if apply_type <= 0 or (apply_type not in [1, 2, 3]):
            return self.ret_json(10006, '申请类型')

        # plan-id
        plan_id = request.values.get('plan_id', '0')
        if not plan_id.isdigit():
            plan_id = 0
        else:
            plan_id = int(plan_id)
        if plan_id <= 0:
            return self.ret_json(10005, '方案ID为空')

        if apply_type in [2, 3]:
            # 产品ID
            product_id = request.values.get('product_id', "0")
            if not product_id.isdigit():
                product_id = 1
            else:
                product_id = int(product_id)
            if product_id <= 0:
                return self.ret_json(10003, '产品ID错误')
            # 账号ID
            account_id = request.values.get('account_id', "0")
            if not account_id.isdigit():
                account_id = 1
            else:
                account_id = int(account_id)
            if account_id <= 0:
                return self.ret_json(10004, '账号ID错误')
        else:
            # 方案信息
            plan_info = ProductPlanModel().get_product_plan_info_by_id(plan_id)
            if plan_info is None:
                return self.ret_json(10013, '方案ID错误')
            else:
                account_id = plan_info['account_id']
                product_id = plan_info['product_id']

        # 币种
        currency = str(request.values.get('currency', ''))
        if currency == '' or (currency.upper() not in ['BTC', 'ETH', 'EOS', 'USDT']):
            return self.ret_json(10007, '币种为空或者错误')
        # 申请数量金额
        amount = request.values.get('amount', "0")
        if not self.isfloat(amount):
            amount = 0
        else:
            amount = float(amount)
        if amount <= 0:
            return self.ret_json(10008, '申请数量金额为空')
        # 附件 json
        attachments = request.values.get('attachments', '')
        if attachments == '':
            return self.ret_json(10009, '附件为空')
        list_att = {}
        if attachments:
            list_att = json.loads(attachments)

        if apply_type in [2, 3]:
            # 如果是申请分红和赎回，申请金额不能大于权益金额
            check = Customer.check_amount_valid(plan_id, amount)
            if check is False:
                return self.ret_json(10010, '平仓申请的金额不能大于权益金额')

        else:
            # 申购的金额不能大于可分配金额
            check = Customer.check_buy_amount_valid(account_id, currency, amount)
            if check is False:
                return self.ret_json(10011, '申购申请的金额不能大于权益金额')

        insert = dict()
        insert['customer_id'] = customer_id
        insert['account_id'] = account_id
        insert['product_id'] = product_id
        insert['product_plan_id'] = plan_id
        insert['asset_type'] = asset_type
        insert['apply_type'] = apply_type
        insert['currency'] = currency
        insert['amount'] = amount
        # {'1': '申请中', '2': '成功', '3': '失败'}
        insert['apply_status'] = 1
        insert['user_id'] = user_id
        last_id = ProductPlanTransferModel().add_transfer_model(insert)

        if last_id is False:
            return self.ret_json(10012, '添加失败')
        else:
            # 资金冻结
            # 资金划转
            if apply_type == 1:
                CustomerAccountBalanceModel().account_balance_frozen(customer_id, account_id, currency, amount)
            else:
                # 平仓申请
                ProductPlanModel().plan_balance_frozen(plan_id, amount)

            # 添加附件
            for item in list_att:
                TransferAttachmentsModel().add_transfer_attachments_model(
                    params={"transfer_id": int(last_id), "url": item, "user_id": user_id}
                )
            return self.ret_json(self.ok, self.msg, data={'id': last_id})

    # 检查申请金额是否有效 申请分红和赎回
    @staticmethod
    def check_amount_valid(plan_id, amount):
        plan = ProductPlanModel().get_product_plan_info_by_id(plan_id)
        if plan is None:
            return False
        else:
            balance = float(plan['balance'])
            return True if balance - amount >= 0 else False

    # 检查申请金额是否有效 申请申购
    @staticmethod
    def check_buy_amount_valid(account_id, currency, amount):
        assets = Customer._unallocated_assets(account_id, currency)
        if assets is None:
            return False
        else:
            balance = float(assets['amount'])
            return True if balance - amount >= 0 else False

    # 账号待分配余额 对应币种
    def unallocated_assets(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']
        # 账号ID
        account_id = request.values.get('account_id', "0")
        if not account_id.isdigit():
            account_id = 1
        else:
            account_id = int(account_id)
        if account_id <= 0:
            return self.ret_json(10001, '账号ID错误')

        # 币种
        currency = str(request.values.get('currency', '')).upper()
        if currency == '':
            return self.ret_json(10002, '币种错误')

        all_assets = CustomerAccountBalanceModel().account_balance_info_by_currency(account_id, currency)
        if all_assets is None or all_assets['currency'] is None:
            return self.ret_json(1, 'ok', {
                "currency": currency,
                'amount': '0.0000'
            })
        else:
            assets = {
                "currency": currency,
                'amount': float(all_assets['amount'])
            }
        # 已经分配资金
        allocated_assets = ProductPlanModel().get_product_plan_info_by_aid_and_currency(account_id, currency)
        if allocated_assets is None or (allocated_assets['currency'] is None):
            assets['amount'] = '%.4f' % float(all_assets['amount'])
            return self.ret_json(1, 'ok', assets)
        else:
            allocated_assets = {
                "currency": currency,
                'amount': float(allocated_assets['amount'])
            }
            # 待分配资金
            unallocated_assets = {
                "currency": currency,
                'amount': '%.4f' % (assets['amount'] - allocated_assets['amount'])
            }
            return self.ret_json(1, 'ok', unallocated_assets)

    # 账号待分配余额 对应币种
    @staticmethod
    def _unallocated_assets(account_id, currency):

        all_assets = CustomerAccountBalanceModel().account_balance_info_by_currency(account_id, currency)
        if all_assets is None or all_assets['currency'] is None:
            return False
        else:
            assets = {
                "currency": currency,
                'amount': float(all_assets['amount'])
            }

        # 已经分配资金
        allocated_assets = ProductPlanModel().get_product_plan_info_by_aid_and_currency(account_id, currency)
        if allocated_assets is None or (allocated_assets['currency'] is None):
            assets['amount'] = float(all_assets['amount'])
            return assets
        else:
            allocated_assets = {
                "currency": currency,
                'amount': float(allocated_assets['amount'])
            }
            # 待分配资金
            unallocated_assets = {
                "currency": currency,
                'amount': float(assets['amount'] - allocated_assets['amount'])
            }
            return unallocated_assets
