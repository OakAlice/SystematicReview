## Integrating the csvs pulled from the various databases
import os
import pandas as pd

# combine the three databases and remove the duplicates
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

    # remove duplicates
    combined_df = combined_df.drop_duplicates(subset=['Title'])

    # print to csv
    csv_file_name = os.path.join(folder_path, 'Unique_papers.csv')
    combined_df.to_csv(csv_file_name, index=False)