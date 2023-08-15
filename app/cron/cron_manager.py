from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import app.cron.fetch_new_proxties as fetch_new_proxties


def setup_cron_jobs(context, telegram_api, bot_api):
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        lambda: fetch_new_proxties.start(context, telegram_api),
        trigger=CronTrigger.from_crontab('*/10 * * * *')
    )
    scheduler.start()
