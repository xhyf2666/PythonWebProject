import operator

from flask import render_template, redirect, request, sessions, Blueprint
import json
from service.JobService import JobService
from service.UserService import UserService

jobController = Blueprint("jobController", __name__)


@jobController.route('/getjobsalarybytype', methods=['get', 'post'])
def getJobSalaryByJobType():
    jobService = JobService()
    data = jobService.getJobSalaryByJobType()
    return json.dumps(data, ensure_ascii=False)
    pass


@jobController.route('/getjobcountbytype', methods=['get', 'post'])
def getJobCountByJobType():
    jobService = JobService()
    data = jobService.getJobCountByJobType()
    return json.dumps(data, ensure_ascii=False)
    pass


@jobController.route('/getjobcountbysalary', methods=['get', 'post'])
def getJobCountByJobSalary():
    jobService = JobService()
    data = []
    data.append(jobService.getJobCountByJobSalary(0, 15000))
    data.append(jobService.getJobCountByJobSalary(15000, 30000))
    data.append(jobService.getJobCountByJobSalary(30000, 1000000))

    return json.dumps(data, ensure_ascii=False)


@jobController.route('/getjobcountbycity', methods=['get', 'post'])
def getJobCountByJobCity():
    jobService = JobService()
    data = jobService.getJobCountByJobCity()
    return json.dumps(data, ensure_ascii=False)
    pass


@jobController.route('/getjobhlsalarybytype', methods=['get', 'post'])
def getJobHLSalaryByJobCity():
    jobService = JobService()
    data = jobService.getJobHLSalaryByJobType()
    return json.dumps(data, ensure_ascii=False)
    pass


@jobController.route('/joblist', methods=['post', 'get'])
def joblist():
    searchName = request.form.get("searchName")
    currentPage = request.form.get("currentPage")
    pageSize = request.form.get("pageSize")
    opr = request.form.get("opr")
    jobID = request.form.get("jobID")

    currentPage = 1 if not currentPage else int(currentPage)
    pageSize = 10 if not pageSize else int(pageSize)
    startRow = (currentPage - 1) * pageSize
    page = {"currentPage": currentPage, "pageSize": pageSize, "startRow": startRow}

    search = {}
    if searchName:
        search = {"jobName": searchName}
    searchType = request.form.getlist("jobTypeSelect")
    searchCity = request.form.getlist("jobCitySelect")
    searchLowSalary = request.form.get("searchLowSalary")
    searchHighSalary = request.form.get("searchHighSalary")
    if searchType:
        if "全部" in searchType:
            searchType = None
        else:
            search["jobType"] = searchType
            page["selectType"] = searchType
    if searchCity:
        if "全部" in searchCity:
            searchCity = None
        else:
            search["jobCity"] = searchCity
            page["selectCity"] = searchCity
    if searchLowSalary:
        search["searchLowSalary"] = searchLowSalary
        page["searchLowSalary"] = searchLowSalary
    if searchHighSalary:
        search["searchHighSalary"] = searchHighSalary
        page["searchHighSalary"] = searchHighSalary
    jobService = JobService()
    result = 0
    if opr and opr == "del":
        result = jobService.removeJob(jobID)
        pass
    elif opr and opr == "update":
        jobLowSalary = request.form.get("jobLowSalary")
        jobHighSalary = request.form.get("jobHighSalary")
        jobAverageSalary = (float(jobLowSalary) + float(jobHighSalary)) / 2.0
        data = {"jobID": jobID, "jobLowSalary": jobLowSalary, "jobHighSalary": jobHighSalary,
                "jobAverageSalary": jobAverageSalary}
        result = jobService.updateJob(data)
    elif opr and opr == "add":
        jobCompany = request.form.get("jobCompany")
        jobName = request.form.get("jobName")
        jobCity = request.form.get("jobCity")
        jobType = request.form.get("jobType")
        jobLowSalary = request.form.get("jobLowSalary")
        jobHighSalary = request.form.get("jobHighSalary")
        jobAverageSalary = (float(jobLowSalary) + float(jobHighSalary)) / 2.0

        data = {"jobID": jobID, "jobLowSalary": jobLowSalary, "jobHighSalary": jobHighSalary,
                "jobAverageSalary": jobAverageSalary, "jobCompany": jobCompany, "jobName": jobName, "jobCity": jobCity,
                "jobType": jobType}
        result = jobService.addJob(data)

    pageList, count = jobService.getJobPageList(search, page)
    allType, allCity = jobService.getAllTypeAndCity(search)
    page['pageList'] = pageList
    page['count'] = count
    totalPage = (count // pageSize + (1 if count % pageSize else 0))
    page['totalPage'] = totalPage
    page['allType'] = allType
    page['allCity'] = allCity
    return render_template("joblist.html", page=page, search=search, result=result)


import requests
from lxml import etree
import time


@jobController.route("/scapyjobdetail", methods=['post', 'get'])
def scrapyJobDetail():
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    search = {}
    currentPage = 1
    pageSize = 50
    startRow = 0
    page = {'currentPage': currentPage,
            'pageSize': pageSize,
            'startRow': startRow}
    jobService = JobService()
    pageList, count = jobService.getJobPageList(search, page)
    totalCount = jobService.getCount()  # 总条目数
    while (pageList):

        print(page)
        for row in pageList:
            url = row.get('jobLink')
            detail = row.get("jobDetail")
            if detail != None:
                continue
            header = {"Host": "www.liepin.com", 'Connection': 'close',
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77", }
            print(row.get("jobID"))
            data = {"statusName": "scrapy", "now": row.get("jobID"), "counts": totalCount}
            jobService.updateJobStatus(data)
            response = requests.get(url, headers=header)
            if response.status_code == 200:
                htmlText = response.text
                xtree = etree.HTML(htmlText)
                item = xtree.xpath("/html/body/main/content/section[2]/dl/dd/text()")
                if item:
                    content = item[0]

                    data = {"jobID": row.get("jobID"), "jobDetail": content}
                    jobService.updateJobDetail(data)
                    pass
            time.sleep(3)
            pass
        currentPage += 1
        startRow = (currentPage - 1) * pageSize
        page = {'currentPage': currentPage,
                'pageSize': pageSize,
                'startRow': startRow}
        pageList, count = jobService.getJobPageList(search, page)
    pass
    return json.dumps({"result": "finish"}, ensure_ascii=False)


import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np


@jobController.route("/jobsimilar", methods=['post', 'get'])
def jobSimilar():
    jobService = JobService()
    jobList = jobService.getAllJobList()
    texts = []
    for row in jobList:
        detail = row.get('jobDetail')
        texts.append(" ".join(jieba.cut(detail)))
        pass

    vectorizer = CountVectorizer()
    tf = vectorizer.fit_transform(texts)
    words = vectorizer.get_feature_names()

    tfidfTransformer = TfidfTransformer()

    tfiwf = tfidfTransformer.fit_transform(tf)
    for i in range(len(jobList)):
        job = jobList[i]
        cosine_similarities = linear_kernel(tfiwf[i], tfiwf).flatten()
        top10List = []
        scores = []

        for t in range(11):
            index = np.argmax(cosine_similarities)
            top10List.append(jobList[index])
            scores.append(cosine_similarities[index])
            cosine_similarities[index] = -1
            pass
        # 写入数据库
        for row, score in zip(top10List, scores):
            if row.get('jobID') != job.get('jobID'):
                data = {'jobId': job.get('jobID'), 'similarJobId': row.get('jobID'), 'score': score}
                jobService.addSimilarJob(data)
            pass
        data = {"statusName": "similarJob", "now": i, "counts": len(jobList)}
        jobService.updateJobStatus(data)
    return json.dumps({"result": "finish"}, ensure_ascii=False)
    pass


@jobController.route("/jobdetail", methods=['post', 'get'])
def getJobDetail():
    jobId = request.args.get("jobID")
    jobService = JobService()
    job, sjobList = jobService.getJobDetails(jobId)
    simial = jobService.get_similar_by_id(jobId)
    job_list = list()
    i = 0
    for jobs in sjobList:
        temp = dict()
        temp["jobCompany"] = jobs["jobCompany"]
        char = int(jobs["jobLowSalary"]) / 1000
        temp["jobLowSalary"] = char
        temp["jobID"] = jobs["jobID"]
        temp["similar"] = simial[i]["similar"]
        job_list.append(temp)
        i += 1
    filename = './/static/assets/js/job_similar.json'
    job_list = sorted(job_list, key=operator.itemgetter("jobLowSalary"))
    jsonfile = open(filename, 'w', encoding='utf-8')
    json.dump(job_list, jsonfile, ensure_ascii=False, indent=4)
    return render_template("jobdetail.html", job=job, sjobList=sjobList)
    pass


@jobController.route("/jobstatus", methods=['post', 'get'])
def getJobStatus():
    statusName = request.form.get("statusName")
    jobService = JobService()
    result = jobService.getJobStatus(statusName)
    return result
    pass
