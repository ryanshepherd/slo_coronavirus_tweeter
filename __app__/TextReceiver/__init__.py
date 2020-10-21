import logging
import json
import urllib.parse
import os
import re

from __app__ import subscriber_repo

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ["DBConnectionString"]

    try:

        body = req.get_body().decode("utf-8")
        logging.info(body)

        values = parse_form_values(body)

        if not is_right_message(values["Body"]):
            return func.HttpResponse(f'Text the word "subscribe" if you would like to be added to the SLO Coronavirus Tracker texting list.')

        with subscriber_repo.SubscriberRepository(conn_str) as repo:
            success = repo.add_subscriber(values["From"])

            if not success:
                return func.HttpResponse(f'This number is already subscribed to the SLO Coronavirus Tracker. Reply "stop" to unsubscribe at any time.')

            return func.HttpResponse(f'Added phone number {values["From"]} to the SLO Coronavirus Tracker. Reply "stop" to unsubscribe at any time.')

    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Sorry, something went wrong while processing your request")


def parse_form_values(body: str) -> dict:
    return {item[0] : urllib.parse.unquote(item[1]) for item in [item.split("=") for item in body.split("&")]}

def is_right_message(msg: str) -> bool:
    # Phones and carriers keep finding new ways to mess up the word subscribe
    # Adding a space, adding a plus, etc.
    # Hopefully this catches all the cases.
    return "subscribe" in msg.lower() and "unsubscribe" not in msg.lower()

