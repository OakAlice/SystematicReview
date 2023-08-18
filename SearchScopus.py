## Searching Scopus with the search strings
# using pyScopus that's a wrapper for Scopus API http://zhiyzuo.github.io/python-scopus/

import os
import pandas as pd
from time import sleep

def QueryScopus(ScopusKey, search_strings, output_directory, Num_of_articles):
    from pyscopus import Scopus
    scopus = Scopus(ScopusKey)

    def process_query(query, scopus, Scopus_num_of_articles):
        selected_columns = ['citation_count', 'title', 'year', 'authors', 'full_text']

        try:
            search_df = scopus.search(query, count=Num_of_articles, view="STANDARD")
            
            # Check if the result is None
            if search_df is None:
                raise ValueError("The response from Scopus is None. Check the query or API availability.")
            
            # Check if the result is a DataFrame
            if not isinstance(search_df, pd.DataFrame):
                raise TypeError(f"Expected a DataFrame, but got {type(search_df)} instead.")
            
            # Check if the DataFrame is empty
            if search_df.empty:
                return pd.DataFrame(columns=selected_columns)
            
            # Check for missing columns and fill them with NA values
            missing_columns = [col for col in selected_columns if col not in search_df.columns]
            for col in missing_columns:
                search_df[col] = 'NA'

            # Further processing
            search_df['year'] = search_df['cover_date'].str.extract(r'(\d{4})')
            extracted_data = search_df[selected_columns]
            return extracted_data
    
        except KeyError as e:
            return pd.DataFrame(columns=selected_columns)
                 
    search_queries = [' AND '.join(words) for words in search_strings]

    all_results = pd.DataFrame()
    
    i = 0
    for search_query in search_queries:
        # Define the search queries
        query = f"KEY({search_query})"
        try:
            processed_data = process_query(query, scopus, Num_of_articles)
            if not processed_data.empty:  
                all_results = pd.concat([all_results, processed_data], ignore_index=True)
        except AttributeError as e:
            continue
        sleep(1)
        
        # Saving to CSV after each search_query
        final_df = all_results.drop_duplicates(subset=['title'])
        
        final_df = final_df.rename(columns={'full_text': 'Link', 'citation_count': 'Citations'})
        final_df.columns = final_df.columns.str.title()
        final_df['Abstract'] = None
        desired_columns = ['Title', 'Authors', 'Year', 'Citations', 'Link', 'Abstract']
        subset = final_df[[col for col in desired_columns if col in final_df.columns]]
        
        csv_file_name = os.path.join(output_directory, f'Scopus_results_{i}.csv')
        subset.to_csv(csv_file_name, index=False)

        i += 1 # iterate higher