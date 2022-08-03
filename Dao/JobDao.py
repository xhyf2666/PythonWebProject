from .BaseDao import BaseDao

class JobDao(BaseDao):
    def createJobData(self,sql,params):
        result=self.execute(sql,params)
        self.commit()
        return result

    def getJobSalaryStaticsByJobType(self):
        sql="select AVG(jobAverageSalary) as jobsavg, jobType from t_job_data group by jobType order by jobsavg"
        result=self.execute(sql)
        return self.fetchall()

    def getJobSalaryStaticsByJobCity(self):
        sql="select AVG(jobAverageSalary) as jobsavg, jobCity from t_job_data group by jobCity order by jobsavg"
        result=self.execute(sql)
        return self.fetchall()

    def getJobCountStatisticByJobType(self):
        sql = "select count(*) as jobCount, jobType from t_job_data group by  jobType order by jobCount desc"
        result = self.execute(sql)
        return self.fetchall()
        pass

    def getJobCountStatisticByJobCity(self):
        sql = "select count(*) as jobCount, jobCity from t_job_data group by  jobCity order by jobCount desc"
        result = self.execute(sql)
        return self.fetchall()
        pass

    def getJobHLSalaryByJobType(self):
        sql = "select AVG(jobAverageSalary) as jobsAvg, jobType,AVG(jobLowSalary) as jobsLow,AVG(jobHighSalary) as jobsHigh from t_job_data group by jobType order by jobsavg"
        result = self.execute(sql)
        return self.fetchall()
        pass

    def getJobPageList(self,search={},page={}):
        sql="select * from t_job_data where 1=1"
        params=[]
        if search.get("jobName"):
            sql += " and jobName like %s "
            params.append("%" + search.get("jobName") + "%")
        sql+=" limit %s,%s"
        params.append(page.get("startRow"))
        params.append(page.get("pageSize"))

        self.execute(sql,params)
        return self.fetchall()

    def getTotalCount(self,search):
        sql="select count(*) as counts from t_job_data where 1=1"
        params=[]
        if search.get("jobName"):
            sql+=" and jobName like %s "
            params.append("%"+search.get("jobName")+"%")
        self.execute(sql,params)
        return self.fetchone()

    def getCount(self):
        sql="select count(*) as counts from t_job_data"
        self.execute(sql)
        return self.fetchone()

    def removeJob(self,jobID):
        sql="DELETE FROM t_job_data WHERE jobID=%s"
        params=[jobID]
        result=self.execute(sql,params)
        self.commit()
        return result

    def updateJob(self,data={}):
        sql="UPDATE t_job_data set jobLowSalary=%s,jobHighSalary=%s,jobAverageSalary=%s where jobID=%s "
        params=[data.get('jobLowSalary'),data.get('jobHighSalary'),data['jobAverageSalary'] ,data.get('jobID')]
        result = self.execute(sql, params)
        self.commit()
        return result

    def addJob(self,data={}):
        sql="INSERT INTO t_job_data (jobCompany,jobName,jobType, jobCity,jobHighSalary,jobLowSalary,jobAverageSalary) VALUES (%s, %s, %s,%s, %s, %s, %s)"
        params = [ data['jobCompany'],data['jobName'],data['jobType'],data['jobCity'],data['jobHighSalary'],data['jobLowSalary'],data['jobAverageSalary']]
        result = self.execute(sql, params)
        self.commit()
        return result

    def updateJobDetail(self,data={}):
        sql="UPDATE t_job_data set jobDetail=%s where jobID=%s "
        params=[data.get('jobDetail'),data.get('jobID')]
        result = self.execute(sql, params)
        self.commit()
        return result

    def getAllJobList(self):
        sql="SELECT * from t_job_data where jobDetail is not null"
        self.execute(sql)
        result=self.fetchall()
        return result

    def addSimilarJob(self, data={}):
        sql = "insert into t_job_similar (jobID, similarJobID, score) values(%s, %s,%s)"
        result = self.execute(sql, [data.get('jobId'), data.get('similarJobId'),data.get('score')])
        self.commit()
        return result
        pass

    # 获取职位详情和相似职位信息
    def getJobDetails(self, id):
        sql = "select * from t_job_data where jobID=%s"
        self.execute(sql, [id])
        job = self.fetchone()
        sql = "select t1.* from  t_job_data t1 where t1.jobID in (select similarJobID from  t_job_similar t2 where t2.jobID=%s)"
        self.execute(sql, [id])
        sjobList = self.fetchall()
        return job, sjobList
        pass

    def updateJobStatus(self,data):
        sql="UPDATE t_job_status set now=%s,counts=%s where statusName=%s "
        params=[data.get('now'),data.get('counts'),data.get('statusName')]
        result = self.execute(sql, params)
        self.commit()
        return result

    def getJobStatus(self,statusName):
        sql="select * from t_job_status where statusName=%s "
        params=[statusName]
        self.execute(sql, params)
        result=self.fetchone()
        self.commit()
        return result