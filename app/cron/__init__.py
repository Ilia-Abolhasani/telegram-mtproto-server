# import app.cron.manager as manager
# import app.cron.job_channel_add_message as job_channel_add_message
# import app.cron.job_channel_edit_message as job_channel_edit_message
# import app.cron.job_connection_analize as job_connection_analize
# import app.cron.job_fetch_new_proxies as job_fetch_new_proxies
import threading
# global variables
# use lock for prevent simultaneously running
job_lock = threading.Lock()
