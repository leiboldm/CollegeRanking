# script to get total expenses from one of 3 different metrics and merge
# total expense data into the main dataset
import pandas

def notNaN(v):
    return v == v

def get_expenses(row):
    if notNaN(row['GASB']):
        return row['GASB']
    if notNaN(row['FASB']):
        return row['FASB']
    if notNaN(row['ForProfit']):
        return row['ForProfit']
    raise Exception("No expenses found for institution {}".format(row['unitid']))

edf = pandas.read_csv("expenses.csv")
cols = list(edf.columns)
cols.remove('year')
cols.remove('name')
edf = edf[cols]
edf['TotalExpenses'] = edf.apply(lambda row: get_expenses(row), axis=1)
edf = edf[['unitid', 'TotalExpenses']]
adf = pandas.read_csv("collegeData.csv")

adf = adf.merge(edf, on='unitid')

print adf.shape

with open("collegeDataV2.csv", "w") as f:
    adf.to_csv(f)
