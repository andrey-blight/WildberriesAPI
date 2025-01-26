import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.core import settings


def send_http_request(artikul: int):
    try:
        response = requests.post(settings.PARSER_URL, json={"artikul": artikul})

        product_json = response.json()



        if response.status_code != 200:
            raise requests.RequestException
    except requests.RequestException:
        pass


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
    'default': ThreadPoolExecutor(10)
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
