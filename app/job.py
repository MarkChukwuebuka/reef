from apscheduler.schedulers.background import BackgroundScheduler
from .utils import formulate_table
from datetime import time
from apscheduler.triggers.cron import CronTrigger


def start():
    scheduler = BackgroundScheduler()
    # Schedule the job to run every day at 1am
    scheduler.add_job(formulate_table, 'cron', hour=1)

    # Start the scheduler
    scheduler.start()