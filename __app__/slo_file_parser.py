from bs4 import BeautifulSoup   # For parsing HTML
import json
import re
from datetime import datetime


def parse_slo_file(content: str):
    page = SloPage(content)

    date = page.update_date
    status = page.get_status()
    cities = page.get_cities()

    # I'm not using this in my texts, so this is just another thing that could break.
    #transmission = page.get_transmission_type()

    # Test details were removed on 9/14
    #tests = page.get_tests()

    return {
        "PartitionKey": "SLO",
        "RowKey": str(date),
        "date": str(date),
        "status": status,
        "cities": cities,
        #"transmission": transmission
        #"tests": tests
    }


class SloPage:
    elements = []


    update_date: datetime

    def __init__(self, content):
        self.content = content
        self.__parse()
        self.update_date = self.__get_date()

        # Extract the first row of data from each chart. Helps identify the chart.
        self.chart_headers = [{"chart_id": item["chart_id"], "headers": str(item["data"][0][0]).lower()} for item in self.elements if item["type"] == "chart"]

    # Must call this to access the state
    def __parse(self):
        # Scanning through the formatted html content, I spotted the data in a script
        soup = BeautifulSoup(self.content, "html.parser")

        # Narrow in on all the <script> tags. The second one has the data of interest.
        script = soup.body.find_all("script")[1].string

        # So "script" contains JavaScript with a single assignment to the variable "infographicData"
        # Let's just get the contents of the assignment into a python JSON variable

        start = script.find("{")
        end = len(script) - 1

        j = json.loads(script[start:end])

        # Now we have a JSON object that describes how to build all the charts
        # All the elements on the page are stored in the "elements" attribute
        self.elements = j["elements"]

    def get_chart_data(self, chart_id):
        return [e["data"] for e in self.elements if e.get("chart_id") == chart_id][0][0]

    def get_chart_data_by_header(self, header):
        chart_id = [item["chart_id"] for item in self.chart_headers if header in item["headers"]][0]
        return self.get_chart_data(chart_id)

    def __get_date(self):
        element = [item for item in self.elements if "particle_type" in item and "bodytitle" in item["particle_type"]][0]
        results = re.search(r"As of (\d+)/(\d+).*/(2\d)", element["text"])
        month = ("00" + results.group(1))[-2:]  # Pad with zeros
        day = ("00" + results.group(2))[-2:]
        year = ("20" + results.group(3))

        return datetime.fromisoformat(f"{year}-{month}-{day}")

    # Extract: Total, Recovered, Deaths, Hospitalized, ICU
    def get_status(self):

        # Prior to (some date), we didn't have access to the simpler time series chart
        if self.update_date < datetime(2020, 8, 16):

            # Use the day's summary chart
            status_chart = self.get_chart_data_by_header("confirmed cases")

            # Turn the status chart into a clean key : value dict
            results = { re.sub("<[^>]+>", "", c[1]): self.__parse_int(re.sub("<[^>]+>", "", c[0]).replace(",", "")) for c in status_chart}

            # Hospitals are like "Hospitalized (2 in ICU): 10". Parse our hospitalized and ICU count.
            k, v = [(k, v) for k, v in results.items() if "hospitalized" in k.lower()][0]
            hospitalized = self.__parse_int(v)
            m = re.search("\((\d+)", k)
            icu = self.__parse_int(m.group(1))

            # Clean it up
            status_dict = {
                "total": self.__parse_int([v for k, v in results.items() if "confirmed" in k.lower()][0]), # Find a key with the word "confirmed"
                "recovered": self.__parse_int([v for k, v in results.items() if "recovered" in k.lower()][0]),
                "deaths": self.__parse_int([v for k, v in results.items() if "death" in k.lower()][0]),
                "hospitalized": hospitalized,
                "icu": icu
            }

        else:
            # Get all the values from the status times series
            status_data = self.get_chart_data_by_header("'recovered'")

            # Label the date column
            if status_data[0][0] == None:
                status_data[0][0] = "Date"

            # Take the headers and hte last row and turn into a dict
            results = {k:v for k, v in zip(status_data[0], status_data[-1])}

            status_dict = {
                "total": self.__parse_int([v for k, v in results.items() if "total" in k.lower()][0]), # Find a key with the word "confirmed"
                "recovered": self.__parse_int([v for k, v in results.items() if "recovered" in k.lower()][0]),
                "deaths": self.__parse_int([v for k, v in results.items() if "death" in k.lower()][0]),
                "hospitalized": self.__parse_int([v for k, v in results.items() if "hospital" in k.lower()][0]),
                "icu": self.__parse_int([v for k, v in results.items() if "icu" == k.lower()][0]), # Don't fuzzy match cause ICU also appears in the hospital label ("hospitalized (non-ICU)")
            }

        # Retrieve test positivity
        try:
            if self.update_date >= datetime(2020, 9, 14):
                stats_list = [item["data"] for item in self.elements if "positivity" in str(item.get("data")).lower()][0][0]
                test_positivity: str = [item for item in stats_list if "positivity" in str(item).lower()][0][0]
                test_positivity = re.search('\d+(\.\d+)?', test_positivity)[0]
                status_dict["test_positivity"] = float(test_positivity)
        # Some days, they just don't publish it, apparently.
        except:
            status_dict["test_positivity"] = None
    
        return status_dict

    # Extract: Case counts by Region
    def get_regions(self):
        
        # Prior to July 3rd, we had regions
        if self.update_date >= datetime(2020, 7, 3):
            raise Exception("Region chart not found on page.")

        region_chart = self.get_chart_data(378110312)
        regions = {self.__standardize_column_name(
            item[0]): self.__parse_int(item[1]) for item in region_chart if item[0].lower() != "region"}

        # Rename "coast" back to "coastal"
        if "coast" in regions.keys():
            regions["coastal"] = regions.pop("coast")

        return regions

    # Extract: Case counts by city
    def get_cities(self):
        city_chart = self.get_chart_data_by_header("'city'")
        cities = {self.__standardize_column_name(
            item[0]): self.__parse_int(item[1]) for item in city_chart if item[0].lower() != "city"}

        return cities

    # extract: Transmission type
    def get_transmission_type(self):
        transmission_chart = self.get_chart_data_by_header("'mode'")
        types = {self.__standardize_column_name(
            item[0]): self.__parse_int(item[1]) for item in transmission_chart if item[0].lower() != "mode"}

        # Rename "under_investigation" back to "unknown"
        if "under_investigation" in types.keys():
            types["unknown"] = types.pop("under_investigation")

        return types

    # Lab testing
    def get_tests(self):
        test_chart = self.get_chart_data_by_header("'lab'")
        tests = {item[0].lower().replace(" ", "_") + "_positive": self.__parse_int(item[1])
                 for item in test_chart if item[0].lower() != "lab"}
        tests.update({item[0].lower().replace(" ", "_") + "_negative": self.__parse_int(item[2])
                 for item in test_chart if item[0].lower() != "lab"})
        return tests

    def __standardize_column_name(self, column: str):
        return re.sub("[()']", "", column.lower().replace(" ", "_").replace("-", "_"))

    def __parse_int(self, value) -> int:
        # Value might be an integer or a string.
        # Either way, convert it to a string, replace commas, and return an int.
        return int(str(value).replace(",", ""))