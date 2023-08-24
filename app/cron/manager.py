from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import app.cron as jobs
import threading

job_lock = threading.Lock()


def start_jobs(context, telegram_api, bot_api):
    scheduler = BackgroundScheduler(
        {'apscheduler.job_defaults.max_instances': 5})
    # job add message to channel
    scheduler.add_job(
        lambda: jobs.job_channel_add_message.start(job_lock, context, bot_api),
        trigger=CronTrigger.from_crontab('*/10 * * * *')
    )

    # job edit last message of channel
    scheduler.add_job(
        lambda: jobs.job_channel_edit_message.start(
            job_lock, context, bot_api),
        trigger=CronTrigger.from_crontab('*/5 * * * *')
    )

    # job test connection of proxy base on reports
    scheduler.add_job(
        lambda: jobs.job_connection_analize.start(job_lock, context),
        trigger=CronTrigger.from_crontab('* * * * *')
    )

    # job fetch new proxies from other proxy chaneels
    scheduler.add_job(
        lambda: jobs.job_fetch_new_proxies.start(
            job_lock, context, telegram_api),
        trigger=CronTrigger.from_crontab('*/15 * * * *')
    )

    scheduler.start()
