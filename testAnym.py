#test script for statistics and privacy markers
import pandas as pd

#load data from xlsx "public_data_registerG.xlsx"
df = pd.read_excel("GroupG/public_data_registerG.xlsx")
print(df.head())