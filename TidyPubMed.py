## tidying the results from the pubmed search
# this script has very minimal changes, but you could do heaps more

import os
import pandas as pd

def TidyingPubMedResults(folder_path):
    file_path = f'{folder_path}/PubMED/PubMed_results.csv'
    df = pd.read_csv(file_path)

    df['Database'] = 'PubMed' # add which database it came from
    df['Citations'] = None # didn't provide citations

    # only select the ones we want (i.e, the ones that other databases had too)
    desired_columns = ['Database', 'Query', 'Title', 'Authors', 'Year', 'Citations', 'Link']
    cols_subset = df[[col for col in desired_columns if col in df.columns]]
    cols_subset = cols_subset.drop_duplicates(subset='Title')

    # print to csv
    csv_file_name = f'{folder_path}/PubMed_collated.csv'
    cols_subset.to_csv(csv_file_name, index=False)
