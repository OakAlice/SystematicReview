import os
import pandas as pd
import re

def CombiningDatabases(output_directory):
    dataframes_list = []

    # Loop through all files in the folder
    for filename in os.listdir(output_directory):
        if filename.endswith('.csv'):
            file_path = f'{output_directory}/{filename}'
            
            # Load each CSV file into a df and append
            df = pd.read_csv(file_path)
            dataframes_list.append(df)

    # Concatenate all df in the list into one df
    combined_df = pd.concat(dataframes_list, ignore_index=True)

    # remove duplicates, retain the ones with abstracts
    combined_df['has_abstract'] = ~combined_df['Abstract'].isnull()
    combined_df.sort_values(by=['has_abstract', 'Title', 'Count'], ascending=[False, True, True], inplace=True)
    combined_df.drop_duplicates(subset=['Title'], keep='first', inplace=True)
    combined_df.drop(columns=['has_abstract'], inplace=True)

    # standardise the formatting of the Query
    # Remove special characters and terms
    def clean_string(s):
        # Remove terms ABS, AND, TITLE, KEY, and strip any parentheses or single quotes
        cleaned = re.sub(r"\bABS\b|\bAND\b|\bTITLE\b|\bKEY\b|[()']", "", s)
        # Split by comma (with optional surrounding spaces)
        keywords = [keyword.strip() for keyword in cleaned.split(",") if keyword.strip()]
        # Return as a single string separated by commas
        return ', '.join(keywords)

    combined_df['Query'] = combined_df['Query'].apply(clean_string)

    # Print to csv
    csv_file_name = f'{output_directory}/Unique_papers.csv'
    combined_df.to_csv(csv_file_name, index=False)
