from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import app.cron as jobs


def start_jobs(context, telegram_api, bot_api):
    scheduler = BackgroundScheduler(
        {'apscheduler.job_defaults.max_instances': 5})
    # job add message to channel
    scheduler.add_job(
        lambda: jobs.job_channel_add_message.start(context, bot_api),
        trigger=CronTrigger.from_crontab('*/3 * * * *')
    )

    # job edit last message of channel
    scheduler.add_job(
        lambda: jobs.job_channel_edit_message.start(context, bot_api),
        trigger=CronTrigger.from_crontab('* * * * *')
    )

    # job test connection of proxy base on reports
    scheduler.add_job(
        lambda: jobs.job_connection_analize.start(context),
        trigger=CronTrigger.from_crontab('*/10 * * * *')
    )

    # job fetch new proxies from other proxy chaneels
    scheduler.add_job(
        lambda: jobs.job_fetch_new_proxies.start(context, telegram_api),
        trigger=CronTrigger.from_crontab('*/15 * * * *')
    )

    scheduler.start()
