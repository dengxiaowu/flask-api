from library.dbmanager import DbManager
from models.base import Base


class CustomerAccountBalanceModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'customer_account_balance'

    # 添加
    def account_balance_add(self, params):
        sql = self.db.sql_crud_generator(table=self.table,
                                         datas=params,
                                         option='insert')
        row = self.db.insert(sql)
        if row:
            return row
        else:
            return False

    # 累计转入
    def account_balance_info(self, customer_account_id):
        sql = self.db.sql_crud_generator(table=self.table,
                                         filters={"customer_account_id": customer_account_id, "status": 0},
                                         datas=['currency', 'amount', 'frozen'],
                                         option='query')
        rows = self.db.fetchall(sql)
        if rows:
            return rows
        else:
            return None

    # 某种类型的累计转入
    def account_balance_info_by_currency(self, customer_account_id, currency):
        sql = self.db.sql_crud_generator(table=self.table,
                                         filters={"customer_account_id": customer_account_id, "currency": currency,
                                                  "status": 0},
                                         datas=['currency', 'amount'],
                                         option='query')
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return None

    # 更新
    def account_balance_update(self, params):
        sql = self.db.sql_crud_generator(table=self.table, datas=params, filters={"id": id, "status": 0},
                                         option='update')
        ret = self.db.execute(sql)

        if ret:
            return ret
        else:
            return False

    # 添加冻结资金
    def account_balance_frozen(self, customer_id, account_id, currency, frozen):

        sql = "update " + self.table + " set frozen = frozen + " + str(
            frozen) + " where status = 0 and customer_id = " + str(customer_id) + " and customer_account_id = " + str(
            account_id) + " and currency = '" + str(currency) + "'"

        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False
