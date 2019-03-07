from library.dbmanager import DbManager
from models.base import Base


# 产品方案转账记录表
class ProductPlanTransferModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'product_plan_transfer'
        self.att_table = 'transfer_attachments'

    def add_transfer_model(self, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, option='insert')
        last_id = self.db.insert(sql)
        if last_id:
            return last_id
        else:
            return False

    def get_transfer_by_id(self, t_id):

        sql = self.db.sql_crud_generator(table=self.table, filters={"id": t_id, "status": 0},
                                         datas=['*'],
                                         option='query',
                                         limit=1)
        row = self.db.fetchone(sql)
        if row is False:
            return None
        else:
            return row

    def update_transfer_model(self, id, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, filters={"id": id, "status": 0},
                                         option='update')
        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False

    def del_transfer_model(self, t_id, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, filters={"id": t_id, "status": 0},
                                         option='update')
        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False

    def get_transfer_list(self, filter_dic, page=1, page_size=20):

        filter_dic['status'] = 0
        sql_total = self.db.sql_crud_generator(table=self.table,
                                               filters=filter_dic,
                                               datas=[
                                                   'id', 'apply_time', 'product_plan_id', 'currency', 'apply_type',
                                                   'amount',
                                                   'apply_status',
                                                   'finish_time', 'cumulative_net_value', 'actual_amount_change',
                                                   'actual_portion_change', 'accumulated_amount',
                                                   'accumulated_portion', 'carry_interest', 'carry_interest_status'],
                                               option='query',
                                               extension={"order": [{"value": "mtime", "desc": True}]},
                                               )

        totals = self.db.fetchall(sql_total)
        if totals is False:
            return {"list": [], "total": 0}

        offset = (page - 1) * page_size

        sql = self.db.sql_crud_generator(table=self.table,
                                         filters=filter_dic,
                                         datas=[
                                             'id', 'apply_time', 'product_plan_id', 'currency', 'apply_type', 'amount',
                                             'apply_status',
                                             'finish_time', 'cumulative_net_value', 'actual_amount_change',
                                             'actual_portion_change', 'accumulated_amount',
                                             'accumulated_portion', 'carry_interest', 'carry_interest_status'],
                                         option='query',
                                         extension={"order": [{"value": "mtime", "desc": True}]},
                                         limit=[offset, page_size])
        rows = self.db.fetchall(sql)

        return {"list": rows, "total": len(totals)}
