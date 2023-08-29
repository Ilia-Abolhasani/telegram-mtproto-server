from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import app.cron.job_channel_add_message as job_channel_add_message
import app.cron.job_channel_edit_message as job_channel_edit_message
import app.cron.job_connection_analize as job_connection_analize
import app.cron.job_fetch_new_proxies as job_fetch_new_proxies


def start_jobs(context, telegram_api, bot_api):
    scheduler = BackgroundScheduler(
        {'apscheduler.job_defaults.max_instances': 5})
    # job add message to channel
    scheduler.add_job(
        lambda: job_channel_add_message.start(context, bot_api),
        trigger=CronTrigger.from_crontab('0 */1 * * *')
    )

    # job edit last message of channel
    scheduler.add_job(
        lambda: job_channel_edit_message.start(context, bot_api),
        trigger=CronTrigger.from_crontab('*/10 * * * *')
    )

    # job test connection of proxy base on reports
    scheduler.add_job(
        lambda: job_connection_analize.start(context),
        trigger=CronTrigger.from_crontab('*/5 * * * *')
    )

    # job fetch new proxies from other proxy chaneels
    scheduler.add_job(
        lambda: job_fetch_new_proxies.start(context, telegram_api),
        trigger=CronTrigger.from_crontab('*/15 * * * *')
    )
    scheduler.start()
