from flask import Flask, render_template, redirect, request, session
from service.UserService import UserService
from service.JobService import JobService
from controller.UserController import userController
from controller.JobController import jobController

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "AFSGGSFAFAS"
app.register_blueprint(userController)
app.register_blueprint(jobController)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['post'])
def login():
    userService = UserService()
    userName = request.form['userName']
    password = request.form['password']
    try:
        user = userService.getUserByUserName(userName)
        if user and user['password'] == password:
            session["user"] = user
            jobService = JobService()
            jobData = jobService.getTopSalaryJobs()
            return render_template('main.html', userName=userName, jobData=jobData)
        else:
            return render_template('index.html', message="密码错误")
    except Exception as e:
        print(e)


# 退出
@app.route("/logout")
def logout():
    session.pop('user')
    session.pop('jobData')
    session.clear()
    return render_template("index.html")
    pass


@app.route("/main")
def toMain():
    jobService = JobService()
    jobData = jobService.getTopSalaryJobs()
    return render_template("main.html", jobData=jobData)
    pass


@app.route("/test")
def ajaxTest():
    return render_template("ajaxTest.html")
    pass


if __name__ == '__main__':
    app.run()
