from library.dbmanager import DbManager
from models.base import Base


class ProductModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'product'

    def add_product_model(self, params):

        sql = "insert into " + self.table + "(`product_name`, `currency`, `capacity`, `user_id`) VALUES (%s, %s, %s, %s)"
        ret = self.db.execute(sql,
                              (params['product_name'], params['currency'], params['capacity'], params['user_id']))

        if ret:
            return ret
        else:
            return False

    def get_product_info_by_name(self, product_name):
        sql = self.db.sql_crud_generator(table=self.table, datas=['*'], option='query',
                                         filters={'product_name': product_name}, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return tuple()

    def get_product_info_by_id(self, id):

        sql = self.db.sql_crud_generator(table=self.table, datas=['id', 'product_name', 'currency', 'capacity'],
                                         option='query',
                                         filters={'id': id}, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return None

    def update_product_model(self, id, params):

        sql = "update " + self.table + " set `capacity` = %s, `user_id` = %s, `mtime` = %s where status = 0 and id = %s"
        ret = self.db.execute(sql,
                              (params['capacity'], params['user_id'], params['mtime'], id))

        if ret:
            return ret
        else:
            return False

    def del_product_model(self, id, params):

        sql = "update " + self.table + " set `status` = %s, `user_id` = %s, `mtime` = %s where status = 0 and id = %s"
        ret = self.db.execute(sql,
                              (params['status'], params['user_id'], params['mtime'], id))

        if ret:
            return ret
        else:
            return False

    def product_list(self):

        sql = self.db.sql_crud_generator(table=self.table, filters={"status": 0},
                                         datas=['id', 'product_name', 'currency', 'capacity'],
                                         option='query')
        rows = self.db.fetchall(sql)

        if rows:
            return rows
        else:
            return False
