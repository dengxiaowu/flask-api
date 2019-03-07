from library.dbmanager import DbManager
from models.base import Base


class ProductPlanModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'product_plan'
        self.product_table = 'product'
        self.customer_table = 'customer'

    def add_product_plan_model(self, params):
        self.db.connect()
        sql = self.db.sql_crud_generator(table=self.table, datas=params, option='insert')
        ret_id = self.db.insert(sql)
        if ret_id:
            return ret_id
        else:
            return False

    def get_product_plan_info_by_id(self, id):

        sql = self.db.sql_crud_generator(table=self.table, filters={"id": id, "status": 0},
                                         datas=['*'],
                                         option='query',
                                         limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return None

    def get_plan_list(self, filter_dic, page=1, page_size=20):

        filter_dic['status'] = 0
        sql_total = self.db.sql_crud_generator(table=self.table,
                                               filters=filter_dic,
                                               datas=[
                                                   'id', 'customer_id', 'account_id', 'product_id', 'plan_name',
                                                   'asset_type', 'currency', 'amount', 'balance'],
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
                                             'id', 'customer_id', 'account_id', 'product_id', 'plan_name',
                                             'asset_type', 'currency', 'amount', 'balance'],
                                         option='query',
                                         extension={"order": [{"value": "mtime", "desc": True}]},
                                         limit=[offset, page_size])
        rows = self.db.fetchall(sql)

        return {"list": rows, "total": len(totals)}

    def update_product_plan_model(self, id, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, filters={"id": id, "status": 0},
                                         option='update')
        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False

    def del_product_plan_model(self, id, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, filters={"id": id, "status": 0},
                                         option='update')
        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False

    # 根据账号ID 获取已经分配的资产
    def get_product_plan_info_by_aid(self, aid):

        sql = self.db.sql_crud_generator(table=self.table, filters={"account_id": aid, "status": 0},
                                         datas=['id', 'customer_id', 'account_id', 'product_id', 'plan_name',
                                                'currency', 'amount',
                                                'balance', 'frozen'],
                                         option='query')
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return None

    # 根据账号ID 获取已经分配的资产 根据币种
    def get_product_plan_info_by_aid_and_currency(self, aid, currency):

        sql = "select currency, sum(amount) as amount from " + self.table + " where account_id = " + str(
            aid) + " and currency = '" + str(currency) + "' and status = 0"
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return None

    # 根据账号ID 获取各个币种已经分配的资产
    def get_product_plans_by_aid(self, aid):

        sql = "select customer_id, account_id, product_id, currency, sum(amount) as amount from " + self.table + " where account_id = " + str(
            aid) + " and status = 0  group by currency"

        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return None

    def get_product_plan_list_by_cid_and_aid(self, customer_id, account_id):

        sql = self.db.sql_crud_generator(table=self.table,
                                         filters={"customer_id": customer_id, "account_id": account_id, "status": 0},
                                         datas=['id', 'customer_id', 'account_id', 'product_id', 'plan_name'],
                                         option='query')
        rows = self.db.fetchall(sql)
        if rows:
            for row in rows:
                row['plan_id'] = row['id']
                del row['id']
            return rows
        else:
            return None

    def get_product_plan_by_params(self, params):

        sql = self.db.sql_crud_generator(table=self.table, filters=params,
                                         datas=['id'],
                                         option='query')
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return None

    def get_plan_by_name(self, plan_name):

        sql = self.db.sql_crud_generator(table=self.table, filters={"plan_name": plan_name, "status": 0},
                                         datas=['id'],
                                         option='query', limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return None

    def plan_balance_frozen(self, plan_id, frozen):

        sql = "update " + self.table + " set frozen = frozen + " + str(frozen) + " , balance = balance - " + str(
            frozen) + " , amount = amount - " + str(frozen) + " where status = 0 and id = " + str(plan_id)

        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False
