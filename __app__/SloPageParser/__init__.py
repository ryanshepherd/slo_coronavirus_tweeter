import logging
import json
import datetime
import os

import azure.functions as func

from __app__ import slo_file_parser
from . import database


def main(msg: func.QueueMessage, contentStream: func.InputStream, gsheetQueue: func.Out[str], statsQueue: func.Out[str]) -> None:

    conn_string = os.environ["DBConnectionString"]

    # Only process SLO files
    if not msg.get_body().decode("utf-8").endswith("-slo.txt"):
        logging.error("Unrecognized file name. Skipping.")
        return

    try:
        content = contentStream.read()
        data = slo_file_parser.parse_slo_file(content)
        logging.info("Parsed SLO file.")

    except Exception as e:
        logging.error("Failed to parse SLO file.")
        logging.error(e)
        raise

    save_db(data, conn_string)

    statsQueue.set("Database Updated")
    logging.info("Added entry to stats queue.")

    gsheetQueue.set(json.dumps(data))
    logging.info("Added entry to GSheet queue.")

def save_db(data: dict, conn_string: str) -> None:

    date = datetime.date.fromisoformat(data["date"][0:10])

    with database.Database(conn_string) as db:
        db.upsert_row("slo_status", date, data["status"])
        db.upsert_row("slo_cities", date, data["cities"])
        #db.upsert_row("slo_tests", date, data["tests"])
        #db.upsert_row("slo_transmission", date, data["transmission"])
        logging.info("Upserted status, cities")
