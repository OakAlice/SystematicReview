## Searching Scopus with the search strings
# using pyScopus that's a wrapper for Scopus API http://zhiyzuo.github.io/python-scopus/

import os
import pandas as pd

def QueryScopus(ScopusKey, search_strings, output_directory, Scopus_num_of_articles):
    from pyscopus import Scopus
    scopus = Scopus(ScopusKey)

    def process_query(query, scopus, Scopus_num_of_articles):
        selected_columns = ['scopus_id', 'citation_count', 'title', 'year', 'publication_name', 'subtype_description', 'authors', 'full_text', 'query']
        try:
            search_df = scopus.search(query, count=Scopus_num_of_articles, view="STANDARD")
        except KeyError as e:
            print(e)
            return pd.DataFrame(columns=selected_columns)
        # Change the date format
        search_df['year'] = search_df['cover_date'].str.extract(r'(\d{4})')

        # add the keywords that were used
        search_df['query'] = query

        # Select the columns you want
        extracted_data = search_df[selected_columns]

        return extracted_data
         
    search_queries = [' AND '.join(words) for words in search_strings]
    print(len(search_queries))

    all_results = pd.DataFrame()

    for search_query in search_queries:
        # Define the search queries
        search_query_abs = f"ABS({search_query})"
        search_query_title = f"TITLE({search_query})"
        search_query_key = f"KEY({search_query})"

        all_results = pd.DataFrame()

        # Perform the searches and concatenate the results
        for query in [search_query_abs, search_query_title, search_query_key]:
            processed_data = process_query(query, scopus, Scopus_num_of_articles)
            print(processed_data.size)
            if not processed_data.empty:  # only append if processed_data is not empty
                all_results = pd.concat([all_results, processed_data], ignore_index=True)

    final_df = all_results.drop_duplicates(subset=['title'])

    # Apply some column transformations and renaming
    final_df = final_df.rename(columns={'full_text': 'Link', 'citation_count': 'Citations'})
    final_df.columns = final_df.columns.str.title()

    # only select the ones we want (plus empty abstract untill I figure that out)
    final_df['Abstract'] = None
    desired_columns = ['Query', 'Title', 'Authors', 'Year', 'Citations', 'Link', 'Abstract']
    subset = final_df[[col for col in desired_columns if col in final_df.columns]]

    # save to a csv
    csv_file_name = f'{output_directory}\Scopus_results.csv'
    subset.to_csv(csv_file_name, index=False)