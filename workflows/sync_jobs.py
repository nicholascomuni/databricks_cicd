# Databricks notebook source
import json
#import dotenv
import os
import requests
import pandas as pd

# COMMAND ----------

!pip install dotenv

# COMMAND ----------

dotenv.load_dotenv(dotenv.find_dotenv(".env"))
DATABRICKS_WORKSPACE_TOKEN = os.getenv("DATABRICKS_WORKSPACE_TOKEN")
DATABRICKS_WORKSPACE_URL = os.getenv("DATABRICKS_WORKSPACE_URL")

class JobAPI:
    def __init__(self, url, token):
        self.base_url = f"{url}/api/2.0/jobs"
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}

    def list_jobs(self):
        url = f"{self.base_url}/list"
        resp = requests.get(url, headers=self.headers)
        return resp

    def create_job(self, job_settings):
        url = f"{self.base_url}/create"
        resp = requests.post(url, headers=self.headers, json=job_settings)
        return resp

    def update_job(self, job_settings):
        url = f"{self.base_url}/update"
        resp = requests.post(url, headers=self.headers, json=job_settings)
        return resp

    def reset_job(self, job_settings):
        url = f"{self.base_url}/reset"
        resp = requests.post(url, headers=self.headers, json=job_settings)
        return resp

# COMMAND ----------

DATABRICKS_WORKSPACE_URL = 'https://airmiles-ai-prod.cloud.databricks.com'
DATABRICKS_WORKSPACE_TOKEN = 'dapibd179336766147715da826448fcd167d'

url = f"{DATABRICKS_WORKSPACE_URL}/api/2.0/jobs"
headers = {"Authorization": f"Bearer {DATABRICKS_WORKSPACE_TOKEN}"}

list_jobs_url = f"{DATABRICKS_WORKSPACE_URL}/api/2.0/jobs/list"
resp = requests.get(list_jobs_url, headers=headers)
resp

# COMMAND ----------

def jobs_to_pandas(data):
    df_jobs = pd.DataFrame(data["jobs"])
    df_jobs["name"] = df_jobs["settings"].apply(lambda x: x["name"])
    return df_jobs[["job_id", "name"]]

# COMMAND ----------

data = resp.json()

jobs_to_pandas(data)

# COMMAND ----------

def create_or_update_job(
    job_name: str,
    job_settings: dict,
    df_jobs: pd.DataFrame,
    job_client: JobAPI,
):
    if job_name in df_jobs["name"].tolist():
        job_id = df_jobs[df_jobs["name"] == job_name]["job_id"].iloc[0]
        job_id = int(job_id)
        data = {"job_id": job_id, "new_settings": job_settings}
        return job_client.reset_job(data)

    return job_client.create_job(job_settings)

# COMMAND ----------

job_client = JobAPI(DATABRICKS_WORKSPACE_URL, DATABRICKS_WORKSPACE_TOKEN)
data = job_client.list_jobs().json()

df_jobs = jobs_to_pandas(data)
jobs_files = [i for i in os.listdir(".") if i.endswith(".json")]

for i in tqdm(jobs_files):
    job_settings = import_json(i)
    job_name = i.split(".")[0]
    resp = create_or_update_job(job_name, job_settings, df_jobs, job_client)

    if resp.status_code != 200:
        print(i, resp.text)

# COMMAND ----------

from tqdm import tqdm

for i in tqdm(range(10000000)):
    pass
