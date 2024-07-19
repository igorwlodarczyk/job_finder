from bs4 import BeautifulSoup
from job_finder.config import capgemini_jobs_search
from job_finder.common import get_html_with_playwright


def get_available_job_positions_capgemini() -> list:
    """
    Retrieves a list of available job positions from the Capgemini website.

    This function scrapes job positions from the Capgemini careers page by:
    1. Fetching the HTML content of the page using a Playwright script.
    2. Parsing the HTML content with BeautifulSoup to extract job position titles.
    3. Cleaning and formatting the titles to return a list of job positions.

    :return: A list of strings, where each string represents a job position title.
    :rtype: list
    """
    html = get_html_with_playwright(capgemini_jobs_search)
    soup = BeautifulSoup(html, "html.parser")
    position_divs = soup.find_all("div", class_="table-td table-title")

    positions = [
        position_div.get_text(strip=True).replace("Nazwa stanowiska", "")
        for position_div in position_divs
    ]
    return positions
