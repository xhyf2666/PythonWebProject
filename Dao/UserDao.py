from .BaseDao import BaseDao

class UserDao(BaseDao):
    def getUserByUserName(self,userName):
        sql="select * from t_user where userName=%s"
        params=[userName]
        self.execute(sql,params=params)
        return self.fetchone()

    def getAllUserList(self):
        sql="select * from t_user"
        self.execute(sql)
        return self.fetchall()

    def getUserPageList(self,search={},page={}):
        sql="select * from t_user where 1=1"
        params=[]
        if search.get("userName"):
            sql += " and userName like %s "
            params.append("%" + search.get("userName") + "%")
        sql+=" limit %s,%s"
        params.append(page.get("startRow"))
        params.append(page.get("pageSize"))

        self.execute(sql,params)
        return self.fetchall()

    def getTotalCount(self,search):
        sql="select count(*) as counts from t_user where 1=1"
        params=[]
        if search.get("userName"):
            sql+=" and userName like %s "
            params.append("%"+search.get("userName")+"%")
        self.execute(sql,params)
        return self.fetchone()

    def removeUser(self,userID):
        sql="DELETE FROM t_user WHERE userID=%s"
        params=[userID]
        result=self.execute(sql,params)
        self.commit()
        return result

    def updateUser(self,data={}):
        sql="UPDATE t_user set realName=%s where userId=%s "

        print(data)
        params=[data.get('realName'), data.get('userID')]
        result = self.execute(sql, params)
        print(result)
        self.commit()
        return result

    def addUser(self,data={}):
        sql="INSERT INTO t_user (userName, password, realName) VALUES (%s, %s, %s)"
        params = [ data['userName'],data['password'],data['realName']]
        result = self.execute(sql, params)
        self.commit()
        return result

    def close(self):
        super().close()