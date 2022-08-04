from service.JobService import JobService
import json
jobser = JobService()
job, sjobList = jobser.getJobDetails("1")
job_list = list()
for jobs in sjobList:
    temp = dict()
    temp["jobCompany"] = jobs["jobCompany"]
    char = int(jobs["jobLowSalary"]) / 1000
    temp["jobLowSalary"] = char
    job_list.append(temp)
job_json = json.dumps(job_list, ensure_ascii=False)
print(job_json)
