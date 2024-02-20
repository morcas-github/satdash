import pandas as pd

# read in satellites db as xlsx found on site.
# sidenote: .txt had issues with recognizing columns, presumably formatting issues.
sats = pd.read_excel("UCS-Satellite-Database-1-1-2023.xlsx")


sats = sats.loc[:, :'Source.6']
sats = sats.drop(columns=["Unnamed: 28"])
for col in sats.columns:
    print(col)

sats["Perigee (km)"] = sats["Perigee (km)"].replace(",", "", regex=True)
sats["Apogee (km)"] = sats["Apogee (km)"].replace(",", "", regex=True)
sats["Launch Mass (kg.)"] = sats["Launch Mass (kg.)"].replace(",", "", regex=True)
sats["Dry Mass (kg.)"] = sats["Dry Mass (kg.)"].replace(",", "", regex=True)

sats.to_csv("sat-db-clean.csv", index=False)