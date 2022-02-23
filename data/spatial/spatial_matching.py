import pandas as pd
import os

"""
This stages loads a file containing spatial codes inside a pre-defined area to use as a matching column between
 census and HTS data
 """

SOURCE = "iris_2017/spatial_matching.csv"


def configure(context):
    context.config("data_path")


def execute(context):
    df_spatial_matching = pd.read_csv("%s/%s" % (context.config("data_path"), SOURCE), encoding="UTF8",
                                      usecols=["IRIS", "ZONE"], dtype={"IRIS": str, "ZONE": int})

    return df_spatial_matching


def validate(context):
    if not os.path.exists("%s/%s" % (context.config("data_path"), SOURCE)):
        raise RuntimeError("Spatial matching data is not available")

    return os.path.getsize("%s/%s" % (context.config("data_path"), SOURCE))
