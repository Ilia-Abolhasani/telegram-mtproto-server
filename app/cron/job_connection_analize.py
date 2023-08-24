def start(job_lock, context):
    with job_lock:
        context.proxies_connection_update()
