## Searching PubMed for even more citations yay
# tutorial from https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/

import pandas as pd
import time
from Bio import Entrez
from requests.exceptions import HTTPError
from urllib.error import HTTPError as urlHTTPERROR
from time import sleep
import http.client

def QueryPubMed(search_strings, Num_of_articles, output_directory, PubMedEmail):
    # Set email (required by NCBI API)
    Entrez.email = PubMedEmail

    def search(query):
        try:
            handle = Entrez.esearch(db='pubmed', 
                                    sort='relevance', 
                                    retmax='20',
                                    retmode='xml', 
                                    term=query)
            results = Entrez.read(handle)
            sleep(1/3) 
            return results
        except HTTPError as e:
            print("An error occurred while searching:", e)
            sleep(1/3)
            return None

    def fetch_details(id_list, max_retries=3):
        for attempt in range(max_retries):
            try:
                if not id_list:
                    return None
                
                ids = ','.join(id_list)
                handle = Entrez.efetch(db='pubmed',
                                    retmode='xml',
                                    id=ids)
                results = Entrez.read(handle)
                sleep(1/3)  # Ensure we don't exceed 3 queries per second
                return results
            except urlHTTPERROR as e:
                print(f"Bad HTTP request for {id_list}. Error: {e}")
                return None
            except HTTPError as e:
                print("An error occurred while fetching details:", e)
                sleep(1/3) 
            except http.client.IncompleteRead:
                # If we got an IncompleteRead error, we wait a bit and retry
                print("Incomplete read error. Retrying...")
                sleep(2)  # Wait for 2 seconds before retrying
                continue
        # If we've exhausted our retries and still haven't succeeded, return None
        print(f"Failed to fetch details after {max_retries} attempts.")
        return None

    def process_searches(search_strings, Num_of_articles, output_directory):
        search_queries = [' AND '.join(words) for words in search_strings]

        all_papers = []
        for query in search_queries:
            results = search(query)
            
            if results and 'IdList' in results and len(results['IdList']) > 0:
                id_list = results['IdList'][:Num_of_articles]
                papers = fetch_details(id_list)
                if papers is None: # skip if bad request
                    continue
                if papers and 'PubmedArticle' in papers:
                    for j, paper in enumerate(papers['PubmedArticle']):
                        title = paper['MedlineCitation']['Article']['ArticleTitle']
                        authors = ', '.join([author['LastName'] for author in paper['MedlineCitation']['Article']['AuthorList']])
                        year_list = paper['MedlineCitation']['Article']['ArticleDate']
                        year = year_list[0].get('Year', '') if year_list else ''
                        link = f"https://www.ncbi.nlm.nih.gov/pubmed/{paper['MedlineCitation']['PMID']}"

                        abstract_section = paper['MedlineCitation']['Article'].get('Abstract', None)
                        if abstract_section and 'AbstractText' in abstract_section:
                            abstract = ''.join(abstract_section['AbstractText'])
                        else:
                            abstract = 'N/A'
 

                        all_papers.append({
                            "Title": title,
                            "Authors": authors,
                            "Year": year,
                            "Link": link,
                            "Abstract": abstract
                        })
                        sleep(1/3)  # Ensure we don't exceed 3 queries per second

                # save into a dataframe and edit the structure and columns a little
                df = pd.DataFrame(all_papers)
                df['Citations'] = None # didn't provide citations
                
                # only select the columns we want
                desired_columns = ['Query', 'Title', 'Authors', 'Year', 'Citations', 'Link', 'Abstract']
                cols_subset = df[[col for col in desired_columns if col in df.columns]]
                
                # drop the duplicates
                cols_subset = cols_subset.drop_duplicates(subset='Title')
                
                # save as a csv
                filename = f'{output_directory}/PubMed_results.csv'
                df.to_csv(filename, index=False)  # Save DataFrame to CSV file
        return all_papers
    
    return process_searches(search_strings, Num_of_articles, output_directory)