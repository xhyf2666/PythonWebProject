from Dao.UserDao import UserDao

class UserService():



    def getUserByUserName(self,userName):
        userDao = UserDao()
        try:
            user = userDao.getUserByUserName(userName)
        finally:
            userDao.close()
        return user


    def getAllUserList(self):
        userDao=UserDao()
        try:
            userList=userDao.getAllUserList()
        finally:
            userDao.close()
        return userList

    def getUserPageList(self,search,page):
        userDao=UserDao()
        try:
            pageList=userDao.getUserPageList(search,page)
            count=userDao.getTotalCount(search)['counts']
        finally:
            userDao.close()

        return pageList,count

    def removeUser(self,userID):
        userDao=UserDao()
        try:
            result=userDao.removeUser(userID)
        finally:
            userDao.close()

        return result

    def updateUser(self,data):
        userDao=UserDao()
        try:
            result=userDao.updateUser(data)
        finally:
            userDao.close()

        return result

    def addUser(self,data):
        userDao=UserDao()
        try:
            result=userDao.addUser(data)
        finally:
            userDao.close()

        return result