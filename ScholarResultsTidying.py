# Having generated a whole bunch of csvs, we want to tidy the dataframe

import os
import pandas as pd
import re

def TidyingScholarResults(folder_path):

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
    combined_df = combined_df.drop_duplicates(subset=['Title'])

    # Apply some column transformations
    combined_df['Database'] = 'Scholar' # add which database it came from
    combined_df['Query'] = None # the original search string used to find these papers

    # now find the search terms that were used to find the citation
    def get_keywords_from_url(url):
        # Extract the part of the URL after 'q=' parameter
        keywords_match = re.search(r'q=(.*?)&', url)
        if keywords_match:
            keywords = keywords_match.group(1)
            keywords = keywords.replace('+', ' ')
            keywords = keywords.replace('%20', '_') # underscore it so it stays 1 word
            return keywords
        else:
            return None

    # update the 'Query' column
    combined_df['Query'] = combined_df['Source'].apply(get_keywords_from_url)

    # select the columns shared across the databases
    desired_columns = ['Database', 'Query', 'Title', 'Authors', 'Year', 'Citations', 'Link']
    subset = combined_df[[col for col in desired_columns if col in combined_df.columns]]

    # print to csv
    csv_file_name = os.path.join(folder_path, 'Scholar_collated.csv')
    combined_df.to_csv(csv_file_name, index=False)