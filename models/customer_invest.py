import time

from models.base import Base
from library.dbmanager import DbManager


class CustomerInvestModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'customer_invest'

    def add(self, datas):
        sql = self.db.sql_crud_generator(table=self.table,
                                         datas=datas,
                                         option='insert')
        row = self.db.insert(sql)
        if row:
            return row
        else:
            return False

    def update(self, remark_id, datas):
        datas['mtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = self.db.sql_crud_generator(table=self.table, datas=datas,
                                         option='update', filters={'id': remark_id})
        row = self.db.execute(sql)
        if row:
            return row
        else:
            return False

    def get_info(self, remark_id):
        filters = {'id': remark_id}
        sql = self.db.sql_crud_generator(table=self.table, datas=['*'],
                                         option='query',
                                         filters=filters, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return dict()

    def get_invest_remark_list(self, customer_id):
        sql = self.db.sql_crud_generator(table=self.table, datas=['id', 'customer_id', 'invest_remark'],
                                         option='query', filters={'customer_id': customer_id, 'status': 0})
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return []
