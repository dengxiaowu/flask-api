import time

from library.dbmanager import DbManager
from models.base import Base


class CustomerModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'customer'

    def add_customer_model(self, data):
        sql = self.db.sql_crud_generator(table=self.table,
                                         datas=data,
                                         option='insert')
        last_id = self.db.insert(sql)
        if last_id:
            return last_id
        else:
            return False

    def check_customer_isvalid(self, customer_type, mobile, name, uid=''):
        usr_info = self.get_info_by_id(customer_type, mobile, name, uid)
        if usr_info:
            return 0 == usr_info.get('status')
        else:
            return False

    def get_info_by_id(self, customer_type, mobile, name, uid=''):
        uid = str(uid)
        if len(uid) > 0:
            filters = {'id': uid}
        else:
            filters = {'customer_type': customer_type, 'mobile': mobile} if int(customer_type) == 2 else {
                'customer_type': customer_type, 'name': name}

        sql = self.db.sql_crud_generator(table=self.table, datas=['*'],
                                         option='query',
                                         filters=filters, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return dict()

    def get_info_list(self, page, page_size, filters={'status': 0}):
        page = int(page)
        page_size = int(page_size)
        sql = self.db.sql_crud_generator(table=self.table,
                                         datas=['id', 'customer_type', 'invest_status', 'name', 'business_contact',
                                                'salesrep'],
                                         option='query', extension={"order": [{"value": "mtime", "desc": True}]},
                                         limit=[(page - 1) * page_size, page * page_size], filters=filters)
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return False

    def get_info_total_by_filters(self, filters):
        sql = self.db.sql_crud_generator(table=self.table, datas=['id'],
                                         option='query', filters=filters)
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return []

    def del_by_id(self, uid, admin_id):
        mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = self.db.sql_crud_generator(table=self.table, datas={'status': 1, 'user_id': admin_id, 'mtime': mtime},
                                         option='update', filters={'id': uid})
        row = self.db.execute(sql)
        if row:
            return row
        else:
            return False

    def update_by_id(self, uid, datas):
        datas['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = self.db.sql_crud_generator(table=self.table, datas=datas,
                                         option='update', filters={'id': uid})
        row = self.db.execute(sql)
        if row:
            return row
        else:
            return False
