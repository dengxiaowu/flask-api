import pymysql

from configs.config import configs


class DbManager:
    def __init__(self):
        db_config = configs['mysql']
        self.host = db_config['host']
        self.port = db_config['port']
        self.user = db_config['user']
        self.password = db_config['password']
        self.db = db_config['database']
        self.charset = db_config['charset']
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                        db=self.db,
                                        charset=self.charset)
        except Exception as e:
            return False
        # self.cur = self.conn.cursor()
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        return True

    def close(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    def insert(self, sql, params=None, commit=True, ):
        res = self.connect()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                if commit:
                    lastrowid = self.cur.lastrowid
                    self.conn.commit()
                else:
                    pass
        except Exception as e:
            self.conn.rollback()
            self.close()
            return False
        return lastrowid

    def execute(self, sql, params=None, commit=True, ):
        res = self.connect()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                rowcount = self.cur.execute(sql, params)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except Exception as e:
            self.conn.rollback()
            self.close()
            return False
        return rowcount

    def insert(self, sql, params=None, commit=True, ):
        res = self.connect()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                if commit:
                    lastrowid = self.cur.lastrowid
                    self.conn.commit()
                else:
                    pass
        except Exception as e:
            self.conn.rollback()
            self.close()
            return False
        return lastrowid

    def fetchall(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            return False
        self.close()
        results = self.cur.fetchall()
        return results

    def fetchone(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            return False
        self.close()
        result = self.cur.fetchone()
        return result

    def edit(self, sql, params=None):
        res = self.execute(sql, params, True)
        if not res:
            return False
        self.conn.commit()
        self.close()
        return res

    def filter_func(self, sql, filters):
        if len(filters.keys()) > 1:
            for key in filters.keys():
                if isinstance(filters[key], dict) and 'op' in filters[key].keys() and 'value' in filters[key].keys():
                    if isinstance(filters[key]['value'], int) or isinstance(filters[key]['value'], float):
                        sql += '`{0}`{1}{2} AND '.format(key, filters[key]['op'], filters[key]['value'])
                    else:
                        sql += '`{0}`{1}"{2}" AND '.format(key, filters[key]['op'], filters[key]['value'])
                else:
                    if isinstance(filters[key], int) or isinstance(filters[key], float):
                        sql += '`{0}`={1} AND '.format(key, filters[key])
                    else:
                        sql += '`{0}`="{1}" AND '.format(key, filters[key])
            sql = sql[:-4]
            return sql
        else:
            for key in filters.keys():
                if isinstance(filters[key], dict) and 'op' in filters[key].keys() and 'value' in filters[key].keys():
                    if isinstance(filters[key]['value'], int) or isinstance(filters[key]['value'], float):
                        sql += '`{0}`{1}{2}'.format(key, filters[key]['op'], filters[key]['value'])
                    else:
                        sql += '`{0}`{1}"{2}"'.format(key, filters[key]['op'], filters[key]['value'])
                else:
                    if isinstance(filters[key], int) or isinstance(filters[key], float):
                        sql += '`{0}`={1}'.format(key, filters[key])
                    else:
                        sql += '`{0}`="{1}"'.format(key, filters[key])
            return sql

    def sql_crud_generator(self, table=None, datas=None, option=None, filters=None, limit=None, extension=None):
        """
            option 'insert' params must have table,option,datas
            option 'update' params must have table,option,datas,filters
            option 'query' params must have table,option,datas
            option 'delete' params must have table,option
            param 'filters' type must be dictionary
            param 'limit' must be str digit or int
            param 'extension' must be dictionary and has key order、group, key desc type is bool
            when option is 'query', param 'datas' type must be list or tuple else dictionary
        """
        """
        Advanced functions Example：
            sql_crud_generator(
            table='index', 
            filters={"id": {"op": ">", "value": 2.5}},
            option='query', 
            datas=['*'],
            limit=100,
            extension={"order": [{"value":"update_time","desc":True},{"value":"cons_code","desc":True}], 'group': 'id'}))
        """
        sql = ''
        if table == None or option == None:
            return None
        if filters != None and not isinstance(filters, dict):
            return None

        if option.lower() == 'insert':
            if datas == None:
                return None
            sql = 'INSERT INTO `{0}`'.format(table) + '('
            for key in datas.keys():
                sql += '`{0}`'.format(key) + ','
            sql = sql[:-1] + ')' + ' VALUES ('
            for key in datas.keys():
                sql += '"{0}"'.format(datas[key]) + ','
            sql = sql[:-1] + ')'

        if option.lower() == 'update':
            if filters == {} or filters == None or datas == None:
                return None
            sql = 'UPDATE `{0}` SET '.format(table)
            for key in datas.keys():
                if isinstance(datas[key], int) or isinstance(datas[key], float):
                    sql += '`{0}`={1}'.format(key, datas[key]) + ','
                else:
                    sql += '`{0}`="{1}"'.format(key, datas[key]) + ','
            sql = sql[:-1] + ' WHERE '
            sql = self.filter_func(sql, filters)

        if option.lower() == 'query':
            if datas == None or (not isinstance(datas, tuple) and not isinstance(datas, list)):
                return None
            sql = "SELECT "
            for key in datas:
                sql += '`{0}`,'.format(key)
            sql = sql[:-1] + ' FROM `{0}`'.format(table)
            if filters != None and filters != {}:
                sql += ' WHERE '
                sql = self.filter_func(sql, filters)
            if extension != None and extension != {}:
                if 'group' in extension.keys() and filters != None and filters != {}:
                    sql += ' GROUP BY `{0}`'.format(extension['group'])
                if 'order' in extension.keys():
                    if isinstance(extension['order'], list) and extension['order'] != []:
                        sql += ' ORDER BY '
                        for item in extension['order']:
                            if 'desc' in item.keys() and item['desc']:
                                sql += '`{0}` desc,'.format(item['value'])
                            else:
                                sql += '`{0}`,'.format(item['value'])
                        sql = sql[:-1]
                    else:
                        if 'desc' in extension['order'].keys() and extension['order']['desc']:
                            sql += ' ORDER BY `{0}` desc'.format(extension['order']['value'])
                        else:
                            sql += ' ORDER BY `{0}`'.format(extension['order']['value'])
            if limit != None:
                if isinstance(limit, list) and limit != []:
                    limit = [str(i) for i in limit]
                    if len(limit) > 2:
                        limit = limit[:2]
                    sql += ' LIMIT {0}'.format(','.join(limit))
                else:
                    sql += ' LIMIT {0}'.format(limit)

        if option.lower() == 'delete':
            sql = "DELETE FROM `{0}`".format(table)
            if filters != {} and filters != None:
                sql += ' WHERE '
                sql = self.filter_func(sql, filters)

        return sql
