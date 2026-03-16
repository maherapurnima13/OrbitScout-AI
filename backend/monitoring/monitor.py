from crawlers.intelligence import collect_intelligence
from ai.report_engine import generate_intelligence_report
from database.service import save_report
import datetime

def run_monitor():

    print("OrbitScout monitoring started")

    data = collect_intelligence()

    report = generate_intelligence_report(data)

    timestamp = datetime.datetime.now()

    save_report(
        str(timestamp),
        report["summary"],
        report["insights"]
    )

    print("New intelligence report stored")

    return report