import pandas as pd
import os

"""
This stage loads the raw data of the specified HTS (EDGT Lyon).

Adapted from the first implementation by Valentin Le Besond (IFSTTAR Nantes)
"""


def configure(context):
    context.config("data_path")


HOUSEHOLD_COLUMNS = {
    "ECH": str, "ZFM": str,  # id
    "M6": int, "M21": int, "M14": int,  # number_of_cars, number_of_bikes, number_of_motorbikes
    "COEM": float # weights
}

PERSON_COLUMNS = {
    "ECH": str, "PER": int, "ZFP": str,  # id
    "P2": int, "P4": int,  # sex, age
    "P9": str,  # employed, studies
    "P7": str, "P12": str,  # has_license, has_pt_subscription
    "P11": str,  # socioprofessional_class
    "COEP": float  # weights
}

TRIP_COLUMNS = {
    "ECH": str, "PER": int, "NDEP": int, "ZFD": str,  # id
    "D2A": int, "D5A": int,  # preceding_purpose, following_purpose
    "D3": str, "D7": str,  # origin_zone, destination_zone
    "D4": int, "D8": int,  # time_departure, time_arrival
    "MODP": int, "D11": int, "D12": int  # mode, euclidean_distance, routed_distance
}

SPATIAL_COLUMNS = {"DepCom": str, "ZF__2015": str}

def execute(context):
    # Load households
    df_households = pd.read_csv("%s/edgt_lyon_2015/lyon_2015_std_faf_men.csv" % context.config("data_path"),
                                sep=";", usecols=list(HOUSEHOLD_COLUMNS.keys()), dtype=HOUSEHOLD_COLUMNS)

    # Load persons
    df_persons = pd.read_csv("%s/edgt_lyon_2015/lyon_2015_std_faf_pers.csv" % context.config("data_path"),
                             sep=";", usecols=list(PERSON_COLUMNS.keys()), dtype=PERSON_COLUMNS)

    # Load trips
    df_trips = pd.read_csv("%s/edgt_lyon_2015/lyon_2015_std_faf_depl.csv" % context.config("data_path"),
                           sep=";", usecols=list(TRIP_COLUMNS.keys()), dtype=TRIP_COLUMNS)

    # Load spatial data
    df_spatial = pd.read_csv("%s/edgt_lyon_2015/EDGT 2015 ZF et GP 23 05 2014.csv" % context.config("data_path"),
                             sep=";", usecols=list(SPATIAL_COLUMNS.keys()), dtype=SPATIAL_COLUMNS)

    return df_households, df_persons, df_trips, df_spatial


FILES = ["lyon_2015_std_faf_men.csv", "lyon_2015_std_faf_pers.csv", "lyon_2015_std_faf_depl.csv"]


def validate(context):
    for name in FILES:
        if not os.path.exists("%s/edgt_lyon_2015/%s" % (context.config("data_path"), name)):
            raise RuntimeError("File missing from EDGT: %s" % name)

    return [
        os.path.getsize("%s/edgt_lyon_2015/%s" % (context.config("data_path"), name))
        for name in FILES
    ]
