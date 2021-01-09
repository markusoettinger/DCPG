import pandas as pd
import numpy as np


def run():

    df = pd.read_csv(
        "../publicInfrastructure.csv", parse_dates=["connectionTime"]
    )
    df["ChargingTime[mins]"] = pd.to_timedelta(df["ChargingTime[mins]"], unit="m")
    df_app_csv = df[["userID", "Station_ID", "connectionTime", "ChargingTime[mins]", "DesiredkWh[kWh]"]]
    #time_deviation to simulate difference between estimated and real charging time
    time_deviation = np.random.normal(1.0, 0.15, df_app_csv.shape[0])
    df_app_csv["ChargingTime[mins]"] = df_app_csv["ChargingTime[mins]"] * time_deviation
    df["endtime"] = df["connectionTime"] + df["ChargingTime[mins]"]
    #df["period"] = df.apply(
    #    lambda row: pd.Interval(row["connectionTime"], row["endtime"]), axis=1
    #)
    df_server_csv = df[["userID", "Station_ID", "connectionTime", "endtime", "kWhDelivered[kWh]", "Flex[kWh]"]]
    df_server_csv = df_server_csv.set_index(("endtime")).sort_index()
    df_app_csv = df_app_csv.set_index("connectionTime").sort_index()
    """
    print(df.head(20))
    print(df.info())
    print(df["Flex[kWh]"].sum())
    print(df.groupby(["userID"]).sum())
    print("Station_ID")
    print(df.groupby(["Station_ID"]).sum())
    start_date = df.index[7]
    end_date = df['endtime'][7]
    mask = (df.index >= start_date) & (df.index <= end_date)
    print(df[mask])
    print(df[mask]['Flex[kWh]'].sum())
    """
    return df_app_csv, df_server_csv



if __name__ == "__main__":
    run()
