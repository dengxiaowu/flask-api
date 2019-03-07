import time

from controllers.base import Base
from flask import request
from models.product import ProductModel


class Product(Base):

    def __init__(self):
        super().__init__()

    # 添加
    def product_add(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        product_name = request.values.get('product_name', '')

        if product_name == '':
            return self.ret_json(10001, '产品名字错误或者为空')

        currency = request.values.get('currency', '')
        if currency == '':
            return self.ret_json(10002, '币种错误或者为空')

        capacity = request.values.get('capital_limit', '')
        if capacity == '':
            return self.ret_json(10003, '产品容量错误或者为空')

        # 是否存在
        product_info = ProductModel().get_product_info_by_name(product_name)
        if product_info:
            return self.ret_json(10004, '该产品已经存在')

        insert_dict = dict()
        insert_dict['product_name'] = product_name
        insert_dict['currency'] = currency
        insert_dict['capacity'] = capacity
        insert_dict['user_id'] = user_id
        ret = ProductModel().add_product_model(insert_dict)
        return self.ret_json(1, 'ok', ret)

    def product_info(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        product_id = request.values.get('product_id', '')

        if product_id == '':
            return self.ret_json(10001, 'id为空')

        # 是否存在
        product_info = ProductModel().get_product_info_by_id(product_id)
        if product_info is None:
            return self.ret_json(10002, '该产品不存在')
        else:
            return self.ret_json(1, 'ok', product_info)

    def product_del(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        id = request.values.get('id', '')

        if id == '':
            return self.ret_json(10001, 'id为空')

        # 是否存在
        product_info = ProductModel().get_product_info_by_id(id)
        if product_info is None:
            return self.ret_json(10002, '该产品不存在')
        else:
            update_data = dict()
            update_data['status'] = 1
            update_data['user_id'] = user_id
            update_data['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            ret = ProductModel().del_product_model(id, update_data)

            return self.ret_json(1, 'ok', ret)

    # 更新
    def product_update(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        user_id = token_info['user_id']

        product_id = request.values.get('id', '')
        if product_id == '':
            return self.ret_json(10001, 'id为空')

        capacity = request.values.get('capacity', 0)
        if capacity == 0:
            return self.ret_json(10002, '数量为空')

        # 是否存在
        product_info = ProductModel().get_product_info_by_id(product_id)
        if product_info is None:
            return self.ret_json(10003, '该产品已经存在')

        update_data = dict()
        update_data['capacity'] = capacity
        update_data['user_id'] = user_id
        update_data['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result = ProductModel().update_product_model(product_id, update_data)
        if result is False:
            return self.ret_json(10004, '更新失败')
        return self.ret_json(1, 'ok', result)

    # 列表
    def product_list(self):
        # 操作管理员ID
        token_info = self.check_token()
        if not isinstance(token_info, dict):
            return token_info

        rows = ProductModel().product_list()
        if rows is False:
            return self.ret_json(10001, '产品列表为空')

        for product in rows:
            product['product_id'] = str(product['id'])
            product['currency'] = str(product['currency']).upper()
            product['capacity'] = str(product['capacity'])
            del product['id']

        return self.ret_json(1, 'ok', rows)
