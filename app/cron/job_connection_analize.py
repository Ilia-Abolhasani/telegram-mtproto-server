from app.cron import job_lock


def start(context):
    global job_lock
    with job_lock:
        try:
            context.proxies_connection_update()
        except Exception as error:
            print(error)
            context.session.rollback()
