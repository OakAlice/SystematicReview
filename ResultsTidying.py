# Having generated a whole bunch of csvs, we want to tidy the dataframe

import os
import pandas as pd
import re

# import the csvs from the same place you want to return it to
folder_path = 'C:/Users/oakle/OneDrive/Documents/Systematic Results'

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
combined_df['Database'] = None # add which database it came from
combined_df['Keywords'] = None # the original search string used to find these papers

# check for 'scholar' or 'scopus' in the 'Source' column
def get_database(Source):
    if 'scholar' in Source.lower():
        return 'Scholar'
    elif 'scopus' in Source.lower():
        return 'Scopus'
    else:
        return None
# update the 'Database' column
combined_df['Database'] = combined_df['Source'].apply(get_database)

# now find the search terms that were used to find the citation
def get_keywords_from_url(url):
    # Extract the part of the URL after 'q=' parameter
    keywords_match = re.search(r'q=(.*?)&', url)
    if keywords_match:
        keywords = keywords_match.group(1)
        keywords = keywords.replace('+', ' ')
        keywords = keywords.replace('%20', ' ')
        return keywords
    else:
        return None

# update the 'Keywords' column
combined_df['Keywords'] = combined_df['Source'].apply(get_keywords_from_url)

# print to csv
csv_file_name = os.path.join(folder_path, 'collated.csv')
combined_df.to_csv(csv_file_name, index=False)