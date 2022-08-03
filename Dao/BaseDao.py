import json
import os
import pymysql

class BaseDao():

    def __init__(self,config="mysql_config.json"):
        #path=os.path.split(os.path.realpath(__file__))[0]
        self.__config = json.load(open(os.path.dirname(__file__) + os.sep + config, mode="r", encoding="utf-8"))
        self.__coon=None
        self.__cursor=None
        pass

    def getConnection(self):
        if not self.__coon:
            self.__coon=pymysql.connect(**self.__config)
        return self.__coon

    def execute(self,sql,params=[],ret="dict"):
        result=0
        try:
            self.__coon=self.getConnection()
            if ret=="dict":
                self.__cursor=self.__coon.cursor(pymysql.cursors.DictCursor)   #字典
            else:
                self.__cursor=self.__coon.cursor()                             #元祖

            result=self.__cursor.execute(sql, params)
        except pymysql.DatabaseError as e:
            print(e)
        return result

    def fetchone(self):
        if self.__cursor:
            return self.__cursor.fetchone()

    def fetchall(self):
        if self.__cursor:
            return self.__cursor.fetchall()

    def close(self):
        if self.__cursor:
            self.__cursor.close()

        if self.__coon:
            self.__coon.close()

    def commit(self):
        if self.__coon:
            self.__coon.commit()

    def rollback(self):
        if self.__coon:
            self.__coon.rollback()