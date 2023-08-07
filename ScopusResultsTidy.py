# load in all the individual csvs and stitch them together then remove the duplicates

# Having generated a whole bunch of csvs, we want to tidy the dataframe

import os
import pandas as pd
import re

def TidyingScopusResults(folder_path):

    dataframes_list = []

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(f'{folder_path}/Scholar', filename)
            
            # Load each CSV file into a df and append
            df = pd.read_csv(file_path)
            dataframes_list.append(df)

    # Concatenate all df in the list into one df
    combined_df = pd.concat(dataframes_list, ignore_index=True)

    # remove duplicates
    combined_df = combined_df.drop_duplicates(subset=['title'])

    # Apply some column transformations and renaming
    combined_df['Database'] = 'Scopus' # add which database it came from
    combined_df['Citations'] = None # Scopus didn't provide citations but google scholar did
    combined_df = combined_df.rename(columns={'full_text': 'Link'})
    combined_df.columns = combined_df.columns.str.upper()

    # only select the ones we want (i.e, the ones that other databases had too)
    desired_columns = ['Database', 'Query', 'Title', 'Authors', 'Year', 'Citations', 'Link']
    subset = combined_df[[col for col in desired_columns if col in combined_df.columns]]

    # print to csv
    csv_file_name = os.path.join(folder_path, 'Scopus_collated.csv')
    combined_df.to_csv(csv_file_name, index=False)