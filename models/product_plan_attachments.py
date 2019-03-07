from library.dbmanager import DbManager
from models.base import Base


class ProductPlanAttachModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'product_plan_attachments'

    def add_attachments_model(self, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, option='insert')
        last_id = self.db.insert(sql)
        if last_id:
            return last_id
        else:
            return False

    def get_attachments_by_id(self, id):

        sql = self.db.sql_crud_generator(table=self.table, filters={"id": id, "status": 0},
                                         datas=['*'],
                                         option='query',
                                         limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return None

    def del_attachments_model(self, id, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, filters={"id": id, "status": 0},
                                         option='update')
        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False

    def get_attachments_by_plan_id(self, plan_id):

        sql = self.db.sql_crud_generator(table=self.table, filters={"product_plan_id": plan_id, "status": 0},
                                         datas=['id', 'product_plan_id', 'url'],
                                         option='query')
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return []
