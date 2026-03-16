from database.db import SessionLocal, engine
from database.models import Base, IntelligenceReport

Base.metadata.create_all(bind=engine)

def save_report(timestamp, summary, insights):

    db = SessionLocal()

    report = IntelligenceReport(
        timestamp=timestamp,
        summary=summary,
        insights=str(insights)
    )

    db.add(report)

    db.commit()

    db.close()


def get_reports():

    db = SessionLocal()

    reports = db.query(IntelligenceReport).all()

    db.close()

    return reports