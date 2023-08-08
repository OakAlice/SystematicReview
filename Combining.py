import os
import pandas as pd

def CombiningDatabases(folder_path):
    dataframes_list = []

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = f'{folder_path}/{filename}'
            
            # Load each CSV file into a df and append
            df = pd.read_csv(file_path)
            dataframes_list.append(df)

    # Concatenate all df in the list into one df
    combined_df = pd.concat(dataframes_list, ignore_index=True)

    # Create mapping of titles to PubMed links
    pubmed_links = combined_df[combined_df['Database'] == 'PubMed'].set_index('Title')['Link'].to_dict()

    # Set 'Database' as categorical with 'Scholar' as the last category for priority
    combined_df['Database'] = pd.Categorical(combined_df['Database'], categories=['Scopus', 'PubMed', 'Scholar'], ordered=True)
    
    # Sort and drop duplicates
    combined_df.sort_values(['Title', 'Database'], ascending=[True, True], inplace=True)
    combined_df.drop_duplicates(subset='Title', keep='last', inplace=True)

    # Update the Link column for Google Scholar entries using the mapping
    combined_df.loc[combined_df['Database'] == 'Scholar', 'Link'] = combined_df[combined_df['Database'] == 'Scholar']['Title'].map(pubmed_links).fillna(combined_df['Link'])

    # Print to csv
    csv_file_name = os.path.join(folder_path, 'Unique_papers.csv')
    combined_df.to_csv(csv_file_name, index=False)
