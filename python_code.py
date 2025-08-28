#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 11:31:25 2025

@author: aliemami
"""

# 1. Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.colors import LinearSegmentedColormap

import numpy as np 

# Register the colormap using the new method

# Now you can use the registered colormap by its name
# For example, to set the default colormap for a plot

# Or to use it in a specific plot

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')
# 2. Load the dataset
# Make sure to place the 'Online Retail.csv' file in the same directory as your script
df = pd.read_csv('/name_of_data.csv')

print(df.columns.tolist())
# 3. clean the data 
df.head()
df.shape
df_cleaned=df.dropna()
df_cleaned

df_valid = df_cleaned.copy()
df_valid['IsCanceled'] = df_valid['Invoice'].astype(str).str.startswith('C')
def is_valid_stock(code):
    code = str(code)
    return code[:5].isdigit() and (len(code) == 5 or (len(code) == 6 and code[5].isalpha()))

df_valid['IsValidStockCode'] = df_valid['StockCode'].apply(is_valid_stock)
df_segment_ready = df_valid[
    (~df_valid['IsCanceled']) & (df_valid['IsValidStockCode'])
].copy()

# Optional cleanup
df_segment_ready.drop(['IsCanceled', 'IsValidStockCode'], axis=1, inplace=True)
df_segment_ready.reset_index(drop=True, inplace=True)
df_segment_ready
df_segment_ready[df_segment_ready["Quantity"]<=0]
df_segment_ready[df_segment_ready["Price"]<=0]
df_segment_ready = df_segment_ready[df_segment_ready["Price"] > 0].copy()

# UK analyzing 
df_segment_ready_UK = df_segment_ready[df_segment_ready["Country"]=="United Kingdom"].copy()
# Norway analyzing 
df_segment_ready_Norway = df_segment_ready[df_segment_ready["Country"]=="Norway"].copy()


df_segment_ready_Norway.describe()
df_segment_ready_Norway["Value"] = df_segment_ready_Norway["Price"]* df_segment_ready_Norway["Quantity"]

df_segment_ready_UK.describe()
df_segment_ready_UK["Value"] = df_segment_ready_UK["Price"]* df_segment_ready_UK["Quantity"]


# first plot 


import matplotlib.pyplot as plt
figure, ax = plt.subplots(2,3)

# Assuming your DataFrame is named 'df' and your column is 'column_name'
ax[0,0].hist(df_segment_ready_Norway['Value'], bins=20, edgecolor='black')
# ax[0,0].title('Histogram of Your Data')
ax[0,0].set_xlabel('Value')
ax[0,0].set_ylabel('Frequency')


ax[0,1].hist(df_segment_ready_Norway['Price'], bins=20, edgecolor='black')
# ax[0,0].title('Histogram of Your Data')
ax[0,1].set_xlabel('Price')
# ax[0,1].set_ylabel('Frequency')

ax[0,2].hist(df_segment_ready_Norway['Quantity'], bins=20, edgecolor='black')
# ax[0,0].title('Histogram of Your Data')
ax[0,2].set_xlabel('Quantity')
# ax[0,2].set_ylabel('Frequency')


ax[1,0].hist(np.log( df_segment_ready_Norway['Value']), bins=20, edgecolor='black',color="red")
# ax[0,0].title('Histogram of Your Data')
ax[1,0].set_xlabel('Value')
ax[1,0].set_ylabel('Log Frequency')


ax[1,1].hist(np.log(df_segment_ready_Norway['Price']), bins=20, edgecolor='black',color="red")
# ax[0,0].title('Histogram of Your Data')
ax[1,1].set_xlabel('Price')
# ax[0,1].set_ylabel('Frequency')

ax[1,2].hist(np.log(df_segment_ready_Norway['Quantity']), bins=20, edgecolor='black',color="red")
# ax[0,0].title('Histogram of Your Data')
ax[1,2].set_xlabel('Quantity')
plt.show()

figure.savefig("/Users/aliemami/Movies/SQL/rental/Norway_value.png")
plt.close()
#%%

import matplotlib.pyplot as plt
figure, ax = plt.subplots(1,2)

# Assuming your DataFrame is named 'df' and your column is 'column_name'
ax[0].scatter(df_segment_ready_Norway['Quantity'],df_segment_ready_Norway['Price'])
# ax[0,0].title('Histogram of Your Data')
ax[0].set_xlabel('Quantity')
ax[0].set_ylabel('Price_Norway')


# Assuming your DataFrame is named 'df' and your column is 'column_name'
ax[1].scatter(df_segment_ready_UK['Quantity'],df_segment_ready_UK['Price'],color="red")
# ax[0,0].title('Histogram of Your Data')
ax[1].set_xlabel('Quantity')
ax[1].set_ylabel('Price_UK')

figure.savefig("/Users/aliemami/Movies/SQL/rental/UK_Norway.png")
plt.close()

#%%


df_segment_ready_Norway['InvoiceDate'] = pd.to_datetime(df_segment_ready_Norway['InvoiceDate'])

# Step 2: Group the data by month and calculate the sum of 'Value'
# The `Grouper` function is a great way to group by time periods.
df_monthly = df_segment_ready_Norway.groupby(pd.Grouper(key='InvoiceDate', freq='M'))['Value'].sum().reset_index()



df_segment_ready_UK['InvoiceDate'] = pd.to_datetime(df_segment_ready_UK['InvoiceDate'])
df_monthly_UK = df_segment_ready_UK.groupby(pd.Grouper(key='InvoiceDate', freq='M'))['Value'].sum().reset_index()


# Step 3: Create the plot
figure, ax = plt.subplots(1,2,figsize=(15, 6))

# Plot the monthly sales as a line plot
ax[0].plot(df_monthly['InvoiceDate'], df_monthly['Value'], marker='o', linestyle='-',label="norway")
ax[1].plot(df_monthly_UK['InvoiceDate'], df_monthly_UK['Value'], marker='o', linestyle='-',label="UK",color="red")

# Correct the labels and title
ax[0].set_title('Total Value by Month Norway')
ax[1].set_title('Total Value by Month UK')

ax[0].set_xlabel('Month')
ax[1].set_xlabel('Month')

ax[0].set_ylabel('Total Value')
# plt.le()
# To format the x-axis to show only the month and year
# ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
ax[0].tick_params(axis='x', rotation=45)
ax[1].tick_params(axis='x', rotation=45)

# Show the plot
plt.tight_layout()
plt.show()
figure.savefig("/Users/aliemami/Movies/SQL/rental/UK_Norway_time.png")


