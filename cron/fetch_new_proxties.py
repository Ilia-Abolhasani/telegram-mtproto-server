import schedule

def job():
    print("Cron job is running!")

schedule.every(1).minutes.do(job)