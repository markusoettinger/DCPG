#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%%

#def run():

df = pd.read_csv(
    "./publicInfrastructure.csv", parse_dates=["connectionTime"]
)
df["ChargingTime[mins]"] = pd.to_timedelta(df["ChargingTime[mins]"], unit="m")

df["kWhDelivered/DesiredkWh"] = df["kWhDelivered[kWh]"]/df["DesiredkWh[kWh]"]

df["P[kW]"] = df["kWhDelivered[kWh]"]/(df["ChargingTime[mins]"].dt.total_seconds() / 3600)
#%%
df[df["Flex[kWh]"] > 0 ]["kWhDelivered/DesiredkWh"].hist(bins = 100)
#%%
df[df["Flex[kWh]"] < 0 ]["kWhDelivered/DesiredkWh"].hist(bins = 100)
#%%

x = df["Flex[kWh]"] * -1
y1 = df["kWhDelivered[kWh]"]

fig, ax1 = plt.subplots()
marker_size=0.7
color = 'tab:red'
ax1.set_xlabel('Boost')
ax1.set_ylabel('kWhDelivered', color=color)
ax1.scatter(x, y1, marker_size, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid()
#%%
x = df["Flex[kWh]"] * -1
y2 = df["P[kW]"]
fig, ax2 = plt.subplots()

color = 'tab:blue'
ax2.set_xlabel('Boost')
ax2.set_ylabel('P [kW]', color=color)  # we already handled the x-label with ax1
ax2.scatter(x, y2, marker_size, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.grid()

#%%

x = df["Flex[kWh]"] * -1
y3 = df["kWhDelivered/DesiredkWh"]

fig, ax1 = plt.subplots()
marker_size=0.7
color = 'tab:red'
ax1.set_xlabel('Boost')
ax1.set_ylabel('kWhDelivered/DesiredkWh', color=color)
ax1.scatter(x, y3, marker_size, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid()

#%%
fig.tight_layout()  # otherwise the right y-label is slightly clipped
df.plot()
#%%
