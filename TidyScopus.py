# load in all the individual csvs and stitch them together then remove the duplicates

# Having generated a whole bunch of csvs, we want to tidy the dataframe

import os
import pandas as pd
import re

def TidyingScopusResults(folder_path):

    dataframes_list = []

    # Loop through all files in the folder
    for filename in os.listdir(f'{folder_path}/Scopus'):
        if filename.endswith('.csv'):
            file_path = os.path.join(f'{folder_path}/Scopus', filename)
            
            try:
                # Attempt to Load each CSV file into a df
                df = pd.read_csv(file_path)
                
                # Append df to the list if not empty
                if not df.empty:
                    dataframes_list.append(df)
            except pd.errors.EmptyDataError:
                print(f"File {filename} is empty. Skipping...")
    
    # append the non-empty files together
    if dataframes_list:
        combined_df = pd.concat(dataframes_list, ignore_index=True)
    
    # remove duplicates
    combined_df = combined_df.drop_duplicates(subset=['title'])

    # Apply some column transformations and renaming
    combined_df['Database'] = 'Scopus' # add which database it came from
    combined_df = combined_df.rename(columns={'full_text': 'Link', 'citation_count': 'Citations'})
    combined_df.columns = combined_df.columns.str.title()

    # only select the ones we want (i.e, the ones that other databases had too)
    desired_columns = ['Database', 'Query', 'Title', 'Authors', 'Year', 'Citations', 'Link']
    subset = combined_df[[col for col in desired_columns if col in combined_df.columns]]

    # print to csv
    csv_file_name = f'{folder_path}/Scopus_collated.csv'
    subset.to_csv(csv_file_name, index=False)