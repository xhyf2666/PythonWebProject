from Dao.JobDao import  JobDao

class JobService():

    def getJobSalaryByJobType(self):
        jobDao=JobDao()
        try:
            data=jobDao.getJobSalaryStaticsByJobType()
        finally:
            jobDao.close()
        return data

    def getJobCountByJobType(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobCountStatisticByJobType()
        finally:
            jobDao.close()
        return data

    def getJobCountByJobCity(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobCountStatisticByJobCity()
        finally:
            jobDao.close()
        return data

    def getJobHLSalaryByJobType(self):
        jobDao = JobDao()
        try:
            data = jobDao.getJobHLSalaryByJobType()
        finally:
            jobDao.close()
        return data

    def getJobPageList(self,search,page):
        jobDao = JobDao()
        try:
            pageList=jobDao.getJobPageList(search,page)
            count=jobDao.getTotalCount(search)['counts']
        finally:
            jobDao.close()

        return pageList,count


    def updateJob(self,data):
        jobDao = JobDao()
        try:
            result=jobDao.updateJob(data)
        finally:
            jobDao.close()

        return result

    def updateJobDetail(self,data):
        jobDao = JobDao()
        try:
            result=jobDao.updateJobDetail(data)
        finally:
            jobDao.close()

        return result

    def removeJob(self,jobID):
        jobDao = JobDao()
        try:
            result=jobDao.removeJob(jobID)
        finally:
            jobDao.close()

        return result

    def addJob(self,data):
        jobDao = JobDao()
        try:
            result=jobDao.addJob(data)
        finally:
            jobDao.close()

        return result

    def addSimilarJob(self,data):
        jobDao = JobDao()
        try:
            result=jobDao.addSimilarJob(data)
        finally:
            jobDao.close()

        return result

    def getAllJobList(self):
        jobDao = JobDao()
        try:
            result=jobDao.getAllJobList()
        finally:
            jobDao.close()

        return result

    def getJobDetails(self, id):
        jobDao = JobDao()
        try:
            job, sjobList = jobDao.getJobDetails(id)
        finally:
            jobDao.close()

        return job, sjobList
        pass
    pass

    def updateJobStatus(self,data):
        jobDao = JobDao()
        try:
            result=jobDao.updateJobStatus(data)
        finally:
            jobDao.close()

        return result

    def getCount(self):
        jobDao = JobDao()
        try:
            result=jobDao.getCount()['counts']
        finally:
            jobDao.close()

        return result

    def getJobStatus(self,statusName):
        jobDao = JobDao()
        try:
            result=jobDao.getJobStatus(statusName)
        finally:
            jobDao.close()

        return result