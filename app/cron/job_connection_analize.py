from app.cron import job_lock


def start(context):
    global job_lock
    with job_lock:
        context.proxies_connection_update()
        context.delete_dead_proxies(30)  # todo
