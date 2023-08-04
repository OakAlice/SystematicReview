# load in all the individual csvs and stitch them together then remove the duplicates

# Having generated a whole bunch of csvs, we want to tidy the dataframe

import os
import pandas as pd
import re

# import the csvs from the same place you want to return it to
folder_path = 'C:/Users/oakle/OneDrive/Documents/Systematic Results/Scopus'

dataframes_list = []

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # Load each CSV file into a df and append
        df = pd.read_csv(file_path)
        dataframes_list.append(df)

# Concatenate all df in the list into one df
combined_df = pd.concat(dataframes_list, ignore_index=True)

# Apply some column transformations
combined_df['Database'] = 'Scopus' # add which database it came from

# now find the search terms that were used to find the citation
    # DO THIS LATER

# remove duplicates
combined_df = combined_df.drop_duplicates(subset=['title'])

# print to csv
csv_file_name = os.path.join(folder_path, 'Scopus_collated.csv')
combined_df.to_csv(csv_file_name, index=False)