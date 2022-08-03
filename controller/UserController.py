from flask import render_template,redirect,request,sessions,Blueprint
import json
from service.UserService import UserService
userController=Blueprint('userController',__name__)

@userController.route('/userlist',methods=['post','get'])
def userlist():
    searchName=request.form.get("searchName")
    currentPage=request.form.get("currentPage")
    pageSize=request.form.get("pageSize")
    opr=request.form.get("opr")
    userID=request.form.get("userID")

    currentPage=1 if not currentPage else int(currentPage)
    pageSize=3 if not pageSize else int(pageSize)
    startRow=(currentPage-1)*pageSize
    search={}
    if searchName:
        search={"userName":searchName}
    page={"currentPage":currentPage,"pageSize":pageSize,"startRow":startRow}
    userService=UserService()
    result=0
    if opr and opr=="del":
        result=userService.removeUser(userID)
    elif opr and opr=="update":
        realName=request.form.get("realName")
        data={"userID":userID,"realName":realName}
        result =userService.updateUser(data)
    elif opr and opr=="add":
        realName = request.form.get("realName")
        userName = request.form.get("userName")
        password = request.form.get("password")
        data={"userName":userName,"password":password,"realName":realName}
        result =userService.addUser(data)

    pageList,count=userService.getUserPageList(search,page)
    page['pageList']=pageList
    page['count']=count
    totalPage=(count//pageSize+(1 if count%pageSize else 0))
    page['totalPage']=totalPage
    return render_template("userlist.html",page=page,search=search,result=result)

@userController.route("/ajax",methods=['get','post'])
def ajaxUserList():
    userService=UserService()
    userList=userService.getAllUserList()
    return json.dumps(userList,ensure_ascii=False)