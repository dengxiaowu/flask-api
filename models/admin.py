from library.dbmanager import DbManager
from models.base import Base


class AdminModel(Base):
    def __init__(self):
        super().__init__()
        self.db = DbManager()
        self.table = 'user'

    def add_admin_model(self, username, mobile, password):
        # INSERT INTO students (class_id, name, gender, score) VALUES (2, '大牛', 'M', 80);
        sql = self.db.sql_crud_generator(table=self.table,
                                         datas={'name': username, 'mobile': mobile, 'password': password},
                                         option='insert')
        row = self.db.execute(sql)
        if row:
            return row
        else:
            return False

    def check_user_isvalid(self, mobile, uid=''):
        usr_info = self.get_info_by_mobile(mobile, str(uid))
        if usr_info:
            return 0 == usr_info.get('status')
        else:
            return False

    def get_info_by_mobile(self, mobile, uid=''):
        filters = {'id': uid} if len(uid) > 0 else {'mobile': mobile}
        sql = self.db.sql_crud_generator(table=self.table, datas=['*'],
                                         option='query',
                                         filters=filters, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return dict()

    def get_user_info_by_id(self, uid):
        filters = {'id': uid}
        sql = self.db.sql_crud_generator(table=self.table, datas=['*'],
                                         option='query',
                                         filters=filters, limit=1)
        row = self.db.fetchone(sql)
        if row:
            return row
        else:
            return None
