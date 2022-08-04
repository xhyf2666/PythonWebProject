from Dao.UserDao import UserDao
from WriteLog import WriteLog


class UserService():


    def getUserByUserName(self,userName):
        userDao = UserDao()
        try:
            user = userDao.getUserByUserName(userName)
        except Exception as e:
            WriteLog().ErrorLog(e)
        finally:
            userDao.close()
        return user


    def getAllUserList(self):
        userDao=UserDao()
        try:
            userList=userDao.getAllUserList()
        except Exception as e:
            WriteLog().ErrorLog(e)
        finally:
            userDao.close()
        return userList

    def getUserPageList(self,search,page):
        userDao=UserDao()
        try:
            pageList=userDao.getUserPageList(search,page)
            count=userDao.getTotalCount(search)['counts']
        except Exception as e:
            WriteLog().ErrorLog(e)
        finally:
            userDao.close()

        return pageList,count

    def removeUser(self,userID):
        userDao=UserDao()
        try:
            result=userDao.removeUser(userID)
        except Exception as e:
            WriteLog().ErrorLog(e)
        finally:
            userDao.close()

        return result

    def updateUser(self,data):
        userDao=UserDao()
        try:
            result=userDao.updateUser(data)
        except Exception as e:
            WriteLog().ErrorLog(e)
        finally:
            userDao.close()

        return result

    def addUser(self,data):
        userDao=UserDao()
        try:
            result=userDao.addUser(data)
        except Exception as e:
            WriteLog().ErrorLog(e)
        finally:
            userDao.close()

        return result