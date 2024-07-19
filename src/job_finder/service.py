import os
from datetime import datetime

from job_finder.database import (
    create_database,
    add_job_to_database,
    get_latest_company_available_jobs,
)
from job_finder.company.capgemini import get_available_job_positions_capgemini
from job_finder.notification_handler import send_notification

date = datetime.now().strftime("%Y-%m-%d")
current_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(current_dir, "sqlite.db")

job_search = {"Capgemini": get_available_job_positions_capgemini()}


def run_service():
    if not os.path.exists(db_path):
        create_database(db_path)

    for company_name, job_positions in job_search.items():
        latest_company_available_jobs = get_latest_company_available_jobs(
            db_path, company_name
        )
        for position in job_positions:
            if position not in latest_company_available_jobs:
                send_notification(f"New position at {company_name}! {position}")

            add_job_to_database(db_path, position, company_name, date)


if __name__ == "__main__":
    try:
        run_service()
    except Exception as e:
        log_message = f"{type(e)}: {e}"
        send_notification(log_message)
