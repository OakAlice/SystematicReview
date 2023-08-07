## Searching Scopus with the search strings
# using pyScopus that's a wrapper for Scopus API http://zhiyzuo.github.io/python-scopus/

from pyscopus import Scopus
import os
import pandas as pd
from SearchStrings import search_strings # my variable
from SearchStrings import output_directory
from SearchStrings import Scopus_num_of_articles

# Get an API from Elsevier, you'll need the key.
key = 'fdbb42b4b0363feb81cf4551863b0279'
scopus = Scopus(key)

search_queries = [' AND '.join(words) for words in search_strings]

for j, search_query in enumerate(search_queries):
    try:
        # Define the search queries
        search_query_abs = f"ABS({search_query})"
        search_query_title = f"TITLE({search_query})"
        search_query_key = f"KEY({search_query})"

        # Initialize an empty DataFrame to store the search results
        all_results = pd.DataFrame()

        # Perform the searches and concatenate the results
        for query in [search_query_abs, search_query_title, search_query_key]:
            try:
                search_df = scopus.search(query, count=Scopus_num_of_articles)
                
                # Change the date format
                search_df['year'] = search_df['cover_date'].str.extract(r'(\d{4})')
                
                # add the keywords that were used
                search_df['query'] = query

                # Select the columns you want
                selected_columns = ['title', 'year', 'publication_name', 'subtype_description', 'authors', 'full_text', 'query']
                extracted_data = search_df[selected_columns]            

                # Append the extracted_data to all_results
                all_results = pd.concat([all_results, extracted_data], ignore_index=True)
                
            except Exception as e:
                print("Error:", e)

        # Specify the CSV file name
        csv_file_name = os.path.join(f'{output_directory}/Scopus', f'Scopus_results_{j}.csv')

        # Save the combined search results to a CSV file
        all_results.to_csv(csv_file_name, index=False)

        # Print the CSV file path
        print(csv_file_name)
    except Exception as e:
        print("Error:", e)