import pymysql
from on_shelf_search.settings import DATABASES


class Database_operat(object):
    def __init__(self, database=DATABASES, database_name='default'):
        database_information = database[database_name]
        try:
            self.db = pymysql.connect(host=database_information['HOST'], user=database_information['USER'], port=database_information['PORT'],
                                      password=database_information['PASSWORD'], db=database_information['NAME'])
            self.cur = self.db.cursor()
        except pymysql.err.OperationalError as e:
            print(e)
            print("连接数据库失败")
            return

    #查全部数据
    def search_all(self, sql):
        data= ''
        try:
            self.cur.execute(sql)
            self.db.commit()
            data = self.cur.fetchall()
            print(data)
            data =[i[0] for i in data]
            print(data)
            # data =list(data)
        except pymysql.err.ProgrammingError as e:
            print(e)
            print("查询失败")
        except pymysql.err.InternalError as e :
            print(e)
            print("查询失败")
        # finally:
        #     self.db.close()
        if data:
            return data
        else:
            data = []
            return data
    def close(self):
        self.db.close()
        return


