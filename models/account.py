import time

from library.dbmanager import DbManager
from models.base import Base


class CustomerAccountModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'customer_account'

    # 添加
    def account_add(self, datas):
        sql = self.db.sql_crud_generator(table=self.table,
                                         datas=datas,
                                         option='insert')
        row = self.db.insert(sql)
        if row:
            return row
        else:
            return False

    def account_del(self, account_id, admin_id):
        return self.account_update(account_id, {'status': 1, 'user_id': admin_id})

    # 更新
    def account_update(self, account_id, datas):
        datas['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = self.db.sql_crud_generator(table=self.table, datas=datas,
                                         option='update', filters={'id': account_id})
        row = self.db.execute(sql)
        if row:
            return row
        else:
            return False

    def get_info_by_params(self, customer_id, account_name, api_key, secret_key):
        filters = {'customer_id': customer_id, 'account_name': account_name}
        sql = self.db.sql_crud_generator(table=self.table, datas=['*'],
                                         option='query',
                                         filters=filters, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            filters = {'api_key': api_key, 'secret_key': secret_key}
            sql = self.db.sql_crud_generator(table=self.table, datas=['*'],
                                             option='query',
                                             filters=filters, limit=1)
            row = self.db.fetchone(sql)

        if row:
            return row
        else:
            return dict()

    def get_info_by_customer_id(self, customer_id):
        filters = {'customer_id': customer_id, 'status': 0}
        sql = self.db.sql_crud_generator(table=self.table,
                                         datas=['id', 'customer_id', 'account_type', 'exchange', 'account_name',
                                                'api_key', 'secret_key', 'pass_phrase', 'customer_account',
                                                'customer_password', 'remark'],
                                         option='query',
                                         filters=filters)
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return False

    def get_info_by_account_id(self, account_id):
        filters = {'id': account_id, 'status': 0}
        sql = self.db.sql_crud_generator(table=self.table, datas=['*'],
                                         option='query',
                                         filters=filters, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return False
