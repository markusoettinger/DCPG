import pandas as pd


def run():

    df = pd.read_csv(
        "./publicInfrastructure.csv", parse_dates=["connectionTime"]
    )
    df["ChargingTime[mins]"] = pd.to_timedelta(df["ChargingTime[mins]"], unit="m")
    df["endtime"] = df["connectionTime"] + df["ChargingTime[mins]"]
    df["period"] = df.apply(
        lambda row: pd.Interval(row["connectionTime"], row["endtime"]), axis=1
    )
    df = df.set_index("connectionTime")
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


if __name__ == "__main__":
    run()
