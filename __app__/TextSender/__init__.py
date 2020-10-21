import logging
import os
import json

from __app__ import subscriber_repo

import azure.functions as func


def main(msg: func.QueueMessage, smsMessage: func.Out[str]) -> None:
    conn_string = os.environ["DBConnectionString"]
    texts_enabled = os.environ["EnableTexts"]

    message = msg.get_body().decode("utf-8")
    phones = subscriber_repo.SubscriberRepository(conn_string).get_subscribers()

    texts = []

    for to in phones:
        value = {
            "body": message,
            "to": to
        }
        texts.append(value)

    logging.debug(texts)

    if texts_enabled == "true":
        smsMessage.set(json.dumps(texts))
        logging.info(f'Sent {len(texts)} texts.')
    else:
        logging.info(f'Would have sent {len(texts)} texts.')
