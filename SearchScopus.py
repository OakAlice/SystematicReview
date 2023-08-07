## Searching Scopus with the search strings
# using pyScopus that's a wrapper for Scopus API http://zhiyzuo.github.io/python-scopus/

import os
import pandas as pd

def QueryScopus(ScopusKey, search_strings, output_directory, Scopus_num_of_articles):
    from pyscopus import Scopus
    scopus = Scopus(ScopusKey)

    def process_query(query, scopus, Scopus_num_of_articles):
        search_df = scopus.search(query, count=Scopus_num_of_articles)

        # Change the date format
        search_df['year'] = search_df['cover_date'].str.extract(r'(\d{4})')

        # add the keywords that were used
        search_df['query'] = query

        # Select the columns you want
        selected_columns = ['title', 'year', 'publication_name', 'subtype_description', 'authors', 'full_text', 'query']
        extracted_data = search_df[selected_columns]

        return extracted_data
         
    search_queries = [' AND '.join(words) for words in search_strings]

    for j, search_query in enumerate(search_queries):
        # Define the search queries
        search_query_abs = f"ABS({search_query})"
        search_query_title = f"TITLE({search_query})"
        search_query_key = f"KEY({search_query})"

        all_results = pd.DataFrame()

        # Perform the searches and concatenate the results
        for query in [search_query_abs, search_query_title, search_query_key]:
            processed_data = process_query(query, scopus, Scopus_num_of_articles)
            if not processed_data.empty:  # only append if processed_data is not empty
                all_results = pd.concat([all_results, processed_data], ignore_index=True)

        # Specify the CSV file name
        csv_file_name = os.path.join(f'{output_directory}/Scopus', f'Scopus_results_{j}.csv')

        # Save the combined search results to a CSV file
        all_results.to_csv(csv_file_name, index=False)