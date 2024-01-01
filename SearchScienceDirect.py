# USing the Sciencedirect API

import requests
import csv
from time import sleep
from typing import Any, Dict
from dataclasses import dataclass

from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch


def get_fields_from_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    if entry.get('dc:creator'):
        if isinstance(entry['dc:creator'][0], dict):
            authors = ''.join([author['$'] for author in entry['dc:creator']])
        else:
            authors = ''.join(entry['dc:creator'])
    else:
        authors = 'No authors listed'

    link = entry['link'][0]['@href']
    year = entry['prism:coverDate'].split('-')[0]
    article_id = entry['pii']
    
    DETAIL_URL = f"https://api.elsevier.com/content/article/pii/{article_id}"
    detailed_data = requests.get(DETAIL_URL, headers=headers).json()
    abstract = detailed_data['full-text-retrieval-response']['coredata']['dc:description']

    return {
        "Title": entry['dc:title'],
        "Authors": authors,
        "Year": year,
        "Link": link,
        "Abstract": abstract
    }

# Define a function to search for articles
def QueryScienceDirect(search_strings, Num_of_articles, ScopusKey, output_directory):
    client = ElsClient(api_key=ScopusKey)
    all_papers = []
    
    filename = f'{output_directory}/ScienceDirect_results.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["Query", "Title", "Authors", "Year", "Link", "Abstract"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Write the headers first

    for query in search_strings:
        formatted_query = ' AND '.join(query)
        searchReq = ElsSearch(query=formatted_query, index='scopus') # index='sciencedirect')
        searchReq.execute(els_client=client, count=Num_of_articles, view="STANDARD")
        papers = list(map(lambda entry: get_fields_from_entry, searchReq.results))
        print(f"we got {len(papers)} papers for {query}")
        all_papers.extend(papers)

    with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        for paper in all_papers:
            writer.writerow(paper)

    # headers = {
    #     "X-ELS-APIKey": ScopusKey,
    #     "Accept": "application/json"
    # }
    # all_papers = []
    # MAX_RETRIES = 3  # Define max retries here
    
    # filename = f'{output_directory}/ScienceDirect_results.csv'
    # with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
    #     fieldnames = ["Query", "Title", "Authors", "Year", "Link", "Abstract"]
    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #     writer.writeheader()  # Write the headers first

    # for query in search_strings:
    #     BASE_URL = "https://api.elsevier.com/content/search/sciencedirect"
    #     formatted_query = ' AND '.join(query)
    #     print(formatted_query)

    #     # Make multiple requests for chunks of papers
    #     for start in range(0, Num_of_articles, 50):
    #         parameters = {
    #             "query": formatted_query,
    #             "count": 50,
    #             "start": start 
    #         }

    #         for attempt in range(MAX_RETRIES):
    #             try:
    #                 response = requests.get(BASE_URL, headers=headers, params=parameters)
    #                 data = response.json()
                    
    #                 # Handle case of no results
    #                 if 'search-results' not in data or 'entry' not in data['search-results'] or not data['search-results']['entry']:
    #                     print(f"No results found for query '{formatted_query}' starting at {start}.")
    #                     print(f"THis is the response I got: {data}.")
    #                     break

    #                 for entry in data['search-results']['entry']:
    #                     title = entry['dc:title']
    #                     if entry.get('dc:creator'):
    #                         if isinstance(entry['dc:creator'][0], dict):
    #                             authors = ''.join([author['$'] for author in entry['dc:creator']])
    #                         else:
    #                             authors = ''.join(entry['dc:creator'])
    #                     else:
    #                         authors = 'No authors listed'
    #                     link = entry['link'][0]['@href']
    #                     year = entry['prism:coverDate'].split('-')[0]
    #                     article_id = entry['pii']
                        
    #                     DETAIL_URL = f"https://api.elsevier.com/content/article/pii/{article_id}"
    #                     detailed_data = requests.get(DETAIL_URL, headers=headers).json()
    #                     abstract = detailed_data['full-text-retrieval-response']['coredata']['dc:description']

    #                     all_papers.append({
    #                         "Title": title,
    #                         "Authors": authors,
    #                         "Year": year,
    #                         "Link": link,
    #                         "Abstract": abstract
    #                     })
                    
    #                 # save this chunk to the csv file
    #                 with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
    #                     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #                     for paper in all_papers:
    #                         writer.writerow(paper)
    #                 all_papers.clear()  # Clear the list for the next chunk
    #                 sleep(1/3)

    #             except requests.ConnectionError as e:
    #                 print(f"Error on attempt {attempt + 1}: {e}")
    #                 if attempt == MAX_RETRIES - 1:  # If this was the last attempt
    #                     print("Max retries reached. Skipping this chunk...")
        
    #         sleep(3)  # Wait between chunks

    print(f"Results saved to {filename}.")
