import pandas as pd
import os

"""
This stages loads a file containing spatial codes inside a pre-defined area to filter census and HTS data. 
This filter can be used to prepare a synthetic population for a Metropolitan area for example instead of the whole
department or region
"""

SOURCE = "edgt_lyon_2015/ter_territoire.csv"

def configure(context):
    context.config("data_path")


def execute(context):
    df_iris_metropole = pd.read_csv("%s/%s" % (context.config("data_path"), SOURCE), encoding="UTF8",
                                    usecols=["codeiris", "commune", "insee"], dtype={"codeiris": str})

    df_iris_metropole.columns = ["IRIS", "Name", "INSEE"]
    return df_iris_metropole


def validate(context):
    if not os.path.exists("%s/%s" % (context.config("data_path"), SOURCE)):
        raise RuntimeError("Metropolis data is not available")

    return os.path.getsize("%s/%s" % (context.config("data_path"), SOURCE))
