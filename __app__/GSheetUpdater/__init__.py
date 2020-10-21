import logging
import os
import json
import pathlib

from . import google_sheets

import azure.functions as func


def main(msg: func.QueueMessage) -> None:

    workbook_name = os.environ["GoogleWorkbook"]
    cities_list = os.environ["CitiesList"]

    data = json.loads(msg.get_body())
    
    with open(pathlib.Path(__file__).parent / "../google_client_secret.json", "r") as file:
        client_secret = json.loads(file.read())

    google_sheets.update_sheets(data, cities_list, workbook_name, client_secret)