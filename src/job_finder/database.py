import sqlite3
from datetime import datetime
from pathlib import Path


def create_database(db_path: str | Path):
    """
    Creates a SQLite database with a table named 'jobs' if it does not already exist.

    The 'jobs' table has the following columns:
    - job (TEXT): The title of the job.
    - company (TEXT): The name of the company offering the job.
    - date (DATE): The date the job was added.

    :param db_path: The path to the SQLite database file. Can be a string or a Path object.
    :type db_path: str | Path

    :return: None
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            job TEXT,
            company TEXT,
            date DATE
        )
    """
    )
    conn.commit()
    conn.close()


def add_job_to_database(db_path: str | Path, job: str, company: str, date: str = None):
    """
    Adds a job entry to the database with the provided job title, company name, and date.

    If no date is provided, the current date is used.

    :param db_path: The path to the SQLite database file. Can be a string or a Path object.
    :type db_path: str | Path
    :param job: The title or position of the job to be added (e.g., 'Software Engineer').
    :type job: str
    :param company: The name of the company offering the job (e.g., 'OpenAI').
    :type company: str
    :param date: The date the job was posted or added to the database in 'YYYY-MM-DD' format.
                 If None, the current date will be used.
    :type date: str, optional

    :return: None
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (job, company, date)
        VALUES (?, ?, ?)
        """,
        (job, company, date),
    )

    conn.commit()
    conn.close()


def get_latest_company_available_jobs(db_path: str | Path, company: str) -> list:
    """
    Retrieves the latest available job listings for a specified company from the database.

    This function connects to a SQLite database, finds the most recent date on which jobs
    were posted for the specified company, and then retrieves the job titles for that date.
    If no jobs are found for the specified company, it returns an empty list.

    :param db_path: The path to the SQLite database file. Can be a string or a Path object.
    :type db_path: str | Path
    :param company: The name of the company for which to retrieve the latest job listings.
    :type company: str

    :return: A list of job titles available on the most recent date for the specified company.
    :rtype: list of str
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Find the latest date for the given company
    cursor.execute(
        """
        SELECT MAX(date) FROM jobs
        WHERE company = ?
        """,
        (company,),
    )
    latest_date = cursor.fetchone()[0]

    # If no jobs found for the company, return an empty list
    if latest_date is None:
        conn.close()
        return []

    # Retrieve jobs for the company with the latest date
    cursor.execute(
        """
        SELECT job FROM jobs
        WHERE company = ? AND date = ?
        """,
        (company, latest_date),
    )
    jobs = cursor.fetchall()

    conn.close()

    # Extract job titles from the result
    job_titles = [job[0] for job in jobs]
    return job_titles
