from library.dbmanager import DbManager
from models.base import Base


# 钱包资金流水表
class WalletFlowingModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'wallet_ledger'

    def get_flow_list(self, account_id, page=1, page_size=20):

        filter_dic = {"customer_account_id": account_id, "status": 0}
        sql_total = self.db.sql_crud_generator(table=self.table,
                                               filters=filter_dic,
                                               datas=[
                                                   'id', 'customer_id', 'customer_account_id', 'ledger_id', 'currency',
                                                   'amount', 'typename', 'remark', 'ctime'],
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
                                             'id', 'customer_id', 'customer_account_id', 'ledger_id', 'currency',
                                             'amount', 'typename', 'remark', 'ctime'],
                                         option='query',
                                         extension={"order": [{"value": "mtime", "desc": True}]},
                                         limit=[offset, page_size])

        rows = self.db.fetchall(sql)
        return {"list": rows, "total": len(totals)}

    def update_flow_remark(self, w_id, params):

        sql = self.db.sql_crud_generator(table=self.table, datas=params, filters={"id": w_id, "status": 0},
                                         option='update')
        ret = self.db.execute(sql)
        if ret:
            return ret
        else:
            return False
