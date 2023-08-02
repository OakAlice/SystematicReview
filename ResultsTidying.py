# Having generated a whole bunch of csvs, we want to tidy the dataframe

import os
import pandas as pd

# import the csvs


# Replace 'folder_path' with the path to the folder containing your CSV files
folder_path = 'C:/Users/oakle/OneDrive/Documents/Systematic Results'

# Initialize an empty list to store DataFrames
dataframes_list = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # Load each CSV file into a DataFrame and append
        df = pd.read_csv(file_path)
        dataframes_list.append(df)

# Concatenate all DataFrames in the list into one DataFrame
combined_df = pd.concat(dataframes_list, ignore_index=True)

# Apply some column transformations




# read all the csvs together


# change the 'Source Url' column to be 'Database' and 'search terms' 