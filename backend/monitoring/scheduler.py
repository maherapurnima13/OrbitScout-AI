from apscheduler.schedulers.background import BackgroundScheduler
from monitoring.monitor import run_monitor

scheduler = BackgroundScheduler()

def start_scheduler():

    scheduler.add_job(run_monitor, "interval", minutes=10)

    scheduler.start()

    print("OrbitScout autonomous monitoring started")