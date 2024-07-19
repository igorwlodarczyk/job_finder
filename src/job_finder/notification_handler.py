import http.client, urllib
from decouple import config


app_token = config("APP_TOKEN")
user_key = config("USER_KEY")


def send_notification(message: str):
    """
    Sends a notification using the Pushover API.

    :param message: The message to be sent.
    :type message: str
    """
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(
            {
                "token": app_token,
                "user": user_key,
                "message": message,
            }
        ),
        {"Content-type": "application/x-www-form-urlencoded"},
    )
    conn.getresponse()
