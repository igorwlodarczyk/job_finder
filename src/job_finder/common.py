import requests
from playwright.sync_api import sync_playwright
from job_finder.config import headers, timeout
from time import sleep


def get_html_with_playwright(url: str) -> str:
    """
    Fetches the HTML content of a webpage using Playwright.

    This function uses Playwright to launch a Chromium browser instance, navigate to the specified URL,
    and retrieve the HTML content of the page. The browser is then closed, and Playwright is stopped.

    :param url: The URL of the webpage to fetch.
    :type url: str
    :return: The HTML content of the webpage as a string.
    :rtype: str
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    sleep(1)
    html = page.content()
    browser.close()
    playwright.stop()
    return html


def get_html_with_requests(url: str) -> str:
    """
    Fetches the HTML content of a webpage using the requests library.

    This function sends an HTTP GET request to the specified URL using the requests library and retrieves
    the HTML content of the response.

    :param url: The URL of the webpage to fetch.
    :type url: str
    :return: The HTML content of the webpage as a string.
    :rtype: str
    """
    html = requests.get(url=url, headers=headers, timeout=timeout).text
    return html
