import logging
import os
import requests
import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from __app__.slo_file_parser import SloPage

import azure.functions as func


def main(mytimer: func.TimerRequest, parseQueue: func.Out[str]) -> func.HttpResponse:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
        
    logging.info('Python timer trigger function started at %s', utc_timestamp)

    # Get some environment variables
    storage_conn_string = os.environ["AzureWebJobsStorage"]
    url = os.environ["SloPageUrl"]

    container_name = "corona-page-snapshots"
     
    # Retrieve the page
    logging.info("Retrieving SLO page...")
    content = requests.get(url).content.decode("utf-8")

    # Parse out the actual update date
    date = SloPage(content).update_date.strftime("%Y%m%d")
    logging.info(f"Data was last updated {date}")

    # Assign the filename
    filename = f"{date}-slo.txt"

    # Connect to blob storage
    blob_service_client = BlobServiceClient.from_connection_string(storage_conn_string)
    container_client = blob_service_client.get_container_client(container_name)

    # If file already exists, exit. That means the data has already been processed.
    if filename in [b.name for b in container_client.list_blobs()]:
        logging.info("File already exists. Exiting without saving.")
        return

    # Save the page
    container_client.upload_blob(filename, content)

    # Add an entry to queue
    parseQueue.set(filename)

    logging.info("Saved new page to storage.")
