import logging
import os

from __app__ import stats

import azure.functions as func


def main(msg: func.QueueMessage, textQueue: func.Out[str], tweetQueue: func.Out[str]) -> None:

    conn_string = os.environ["DBConnectionString"]

    # TODO - Check if there's actually any new data to process.

    # Calculate stats on the data.
    message = stats.Stats(conn_string).get_stats()

    # Log the message
    logging.info(message)
    
    # Publish to queues (later: publish to event grid)
    textQueue.set(message)
    tweetQueue.set(message)