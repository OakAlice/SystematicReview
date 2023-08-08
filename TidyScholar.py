# Having generated a whole bunch of csvs, we want to tidy the dataframe

import os
import pandas as pd
import re

def TidyingScholarResults(output_directory):
    file_path = f'{output_directory}/Scholar/results.csv'
    df = pd.read_csv(file_path)

    # remove duplicates
    df = df.drop_duplicates(subset=['Title'])

    # Apply some column transformations
    df['Database'] = 'Scholar' # add which database it came from
    df['Query'] = None # the original search string used to find these papers

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
    df['Query'] = df['Source'].apply(get_keywords_from_url)

    # find the number of citations
    def get_citations_from_string(string):
        match = re.search(r'Cited by (\d+)', string)
        if match:
            citation_number = int(match.group(1))
            return citation_number
        else:
            return "unknown"

    # change the citations row
    df['Citations'] = df['Citations'].apply(get_citations_from_string)

    # select the columns shared across the databases
    desired_columns = ['Database', 'Query', 'Title', 'Authors', 'Year', 'Citations', 'Link']
    subset = df[[col for col in desired_columns if col in df.columns]]

    # print to csv
    csv_file_name = f'{output_directory}/Scholar_collated.csv'
    subset.to_csv(csv_file_name, index=False)