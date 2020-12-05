import psycopg2
import pandas as pd
import numpy as np
import math


class Stats:

    def __init__(self, conn_str: str):
        self.conn = psycopg2.connect(conn_str)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def get_status(self):

        sql = """
            SELECT *
            FROM slo_status
            ORDER BY "date" DESC
            LIMIT 2;
        """

        df = pd.read_sql(sql, self.conn, index_col="date")

        df["active"] = df["total"] - df["recovered"] - df["deaths"]

        update_date = df.index[0]

        status_dict = df.iloc[0].to_dict()
        status_delta = df.fillna(0).diff(periods=-1).iloc[0].astype(int).to_dict()

        return update_date, status_dict, status_delta

    def get_regions(self):

        sql = """
            SELECT 
                "date", 

                COALESCE(san_miguel, 0) + 
                COALESCE(paso_robles, 0) + 
                COALESCE(templeton, 0) + 
                COALESCE(atascadero, 0) + 
                COALESCE(cambria, 0) +
                COALESCE(cayucos, 0) +
                COALESCE(shandon, 0)
                AS north_county,

                COALESCE(arroyo_grande, 0) + 
                COALESCE(nipomo, 0) +
                COALESCE(grover_beach, 0) +
                COALESCE(pismo_beach, 0) +
                COALESCE(oceano, 0)
                AS south_county,

                COALESCE(ca_mens_colony_inmates, 0) + 
                COALESCE(san_luis_obispo_city, 0) +
                COALESCE(avila, 0)
                AS central,

                COALESCE(morro_bay, 0) + 
                COALESCE(los_osos, 0)
                AS coastal
            FROM slo_cities
            ORDER BY "date" DESC
            LIMIT 2;
        """

        df = pd.read_sql(sql, self.conn, index_col="date")

        region_dict = df.iloc[0].to_dict()
        region_delta = df.diff(periods=-1).iloc[0].astype(np.int).to_dict()

        return region_dict, region_delta

    def get_top_cities(self):
                
        sql = """
            SELECT *
            FROM slo_cities
            ORDER BY "date" DESC
            LIMIT 2;
        """

        df = pd.read_sql(sql, self.conn, index_col="date")

        # Pivot the diff
        delta = pd.DataFrame(df.fillna(0).diff(periods=-1).iloc[0].astype(int))

        # Rename the column to 'delta'
        delta = delta.rename(columns={delta.columns[0]: "delta"})

        # Select Top 3 Cities
        topcount = 3
        return delta.sort_values(delta.columns[0], ascending=False)[:topcount] \
            .to_dict()["delta"]

    # def get_test_positivity(self):
        
    #     # Business days over which to measure test positivity
    #     n = 10

    #     sql = f"""
    #         SELECT
    #             "date",
    #             slo_public_health_lab_positive + outside_labs_positive AS total_positive,
    #             slo_public_health_lab_negative + outside_labs_negative AS total_negative
    #         FROM slo_tests
    #         ORDER BY "date" DESC
    #         LIMIT {n};
    #     """

    #     df = pd.read_sql(sql, self.conn, index_col="date")

    #     positive_n_days = df["total_positive"].iloc[0] - \
    #         df["total_positive"].iloc[-1]
    #     total_n_days = df["total_negative"].iloc[0] - \
    #         df["total_negative"].iloc[-1] + positive_n_days

    #     return (positive_n_days / total_n_days) * 100

    def __add_plus(self, value: int):
        return ("+" if value >= 0 else "") + str(value)

    def __rename_city(self, city: str) -> str:
        rename = city.replace("_", " ").title()
        
        switcher = {
            "San Luis Obispo City": "SLO City",
            "Paso Robles": "Paso",
            "Grover Beach": "Grover",
            "Pismo Beach": "Pismo",
            "Arroyo Grande": "A.G.",
            "Ca Mens Colony Inmates": "Mens Colony",
            "Cal Poly Campus Residents": "CalPoly"
        }
       
        return switcher.get(rename, rename)

    def get_stats(self):
        update_date, status_dict, status_delta = self.get_status()
        top_cities = self.get_top_cities()
        #positivity = self.get_test_positivity()

        # Overall
        message = \
            f"{update_date}\n" \
            f"Total: {status_dict['total']} ({self.__add_plus(status_delta['total'])})\n" \
            f"Active: {status_dict['active']} ({self.__add_plus(status_delta['active'])})\n"

        # Deaths
        if status_delta["deaths"] > 0:
            message += f"Deaths: {status_dict['deaths']} ({self.__add_plus(status_delta['deaths'])})\n"

#        # Hospitalizations
#        message += \
#            f"Hospitalized: {status_dict['hospitalized']} ({self.__add_plus(status_delta['hospitalized'])})\n" \
#            f"In ICU: {status_dict['icu']} ({self.__add_plus(status_delta['icu'])})\n" \

        # Top Cities
        message += "\nTop Cities:\n"
        for k, v in top_cities.items():
            message += self.__rename_city(k) + " (+" + str(v) + ")\n"

        # Positivity
        if status_dict['test_positivity'] != None and not math.isnan(status_dict['test_positivity']):
            message += \
                f"\nPositivity: {status_dict['test_positivity']: .2f}%"

        return message