import pandas as pd
import gspread
import re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def update_sheets(data: dict, cities_list: str, workbook_name: str, client_secret: dict) -> None:

    wkb = GWorkbook(workbook_name, client_secret)

    # Convert data to lists
    slo_date = datetime.fromisoformat(data["date"][0:10])

    status = [data["status"][item] for item in ["total", "recovered", "deaths"]]
    cities = [data["cities"].get(city) for city in cities_list.split(",")]
    #tests = [data["tests"].get(attr) for attr in ["slo_public_health_lab_positive", "slo_public_health_lab_negative", "outside_labs_positive", "outside_labs_negative"]]

    # Update SLO Status sheet
    wkb.upsert_sheet(sheet_number=0, 
        date=slo_date,
        data=status,
        copy_columns=["E", "F"])

    # Update SLO Cities sheet
    wkb.upsert_sheet(sheet_number=1, 
        date=slo_date,
        data=cities,
        copy_columns=[])

    # # Update SLO Testing sheet
    # wkb.upsert_sheet(
    #     sheet_number=2, 
    #     date=slo_date,
    #     data=tests,
    #     copy_columns=["F", "G", "H", "I", "J"])


class GWorkbook:

    def __init__(self, workbook_name: str, client_secret: dict) -> None:

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_dict(client_secret, scope)
        client = gspread.authorize(creds)

        self.workbook = client.open(workbook_name)

    def upsert_sheet(self, sheet_number: int, date: datetime, data: [], copy_columns: []):

        # Retrieve the sheet
        sheet = self.workbook.get_worksheet(sheet_number)
        df = pd.DataFrame(sheet.get_all_records())

        last_row = len(df)

        # Check the last update date
        last_updated = datetime.strptime(df.iloc[-1][0], "%m/%d/%Y")

        # If last update same as today, exit
        if last_updated >= date:
            print("Spreadsheet already updated. Exiting.")
            return

        # Otherwise insert the row as (date) + (data)
        row = [self.excel_date(date)] + data
        sheet.insert_row(row, last_row + 2)

        # Format the date cell
        cell = "A" + str(last_row + 2)
        sheet.format(cell, {"numberFormat": {"type": "DATE_TIME", "pattern": "m/d/yyyy"}})

        # Copy the specified columns from the row above
        for col in copy_columns:
            offset = 1

            source_cell = col + str(last_row + 1)
            target_cell = col + str(last_row + 1 + offset)

            formula:str = sheet.acell(source_cell, value_render_option='FORMULA').value
            
            # Update any numbers to numbers + 1
            formula = re.sub("(\d+)", lambda x: str(int(x.group(0)) + offset), formula)

            sheet.update_acell(target_cell, formula)

    def excel_date(self, date1: datetime) -> float:
        temp = datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
        delta = date1 - temp
        return float(delta.days) + (float(delta.seconds) / 86400)

