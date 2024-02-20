import pandas as pd

# display 1000 rows
pd.set_option('display.max_rows', 1000)

# read the csv file in
df = pd.read_csv('sat-db-clean.csv')


# shorthands for column names
country = 'Country of Operator/Owner'
date = 'Date of Launch'
name = 'Current Official Name of Satellite'

# the total number of sats
total = df[country].count()


# these are masks: they're basically boolean evaluations that can be used as index for a df
# the number of sats before 2000
b42kMask = df[date] < '2000-01-01'

# after 2000
aft2kMask = df[date] >= '2000-01-01'

# where country is usa
usaMask = df[country] == 'USA'


# note: not sure if accurate; 
# the goal here was to find the intersection of satellites from USA and satellites made before/after year 2000.
#int_df = pd.merge(df[usaMask], df[b42kMask], how='inner', on=[name])
#int_df_2 = pd.merge(df[usaMask], df[aft2kMask], how='inner', on=[name])

# where country is china
chinaMask = df[country] == 'China'


# the number of satellites whose country is china
chinaCount = len(df[chinaMask])


# a descending sorted list of number of satellites grouped by country.
sortedByCountry = df.groupby(country)[country].count().sort_values(ascending=False)

print(sortedByCountry)