## Searching PubMed for even more citations yay
# tutorial from https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/

import pandas as pd
import time
from Bio import Entrez
from requests.exceptions import HTTPError
from urllib.error import HTTPError as urlHTTPERROR

def QueryPubMed(search_strings, PubMed_num_of_articles, output_directory, PubMedEmail):
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
            return results
        except HTTPError as e:
            print("An error occurred while searching:", e)
            return None

    def fetch_details(id_list):
        try:
            if not id_list:
                return None
            
            ids = ','.join(id_list)
            handle = Entrez.efetch(db='pubmed',
                                retmode='xml',
                                id=ids)
            results = Entrez.read(handle)
            return results
        except urlHTTPERROR as e:
            print(f"Bad HTTP request for {id_list}. Error: {e}")
        except HTTPError as e:
            print("An error occurred while fetching details:", e)
            return None

    def process_searches(search_strings, PubMed_num_of_articles, output_directory):
        search_queries = [' AND '.join(words) for words in search_strings]
        num_of_articles = PubMed_num_of_articles

        all_papers = []
        for query in search_queries:
            results = search(query)
            
            if results and 'IdList' in results and len(results['IdList']) > 0:
                id_list = results['IdList'][:num_of_articles]
                papers = fetch_details(id_list)

                for j, paper in enumerate(papers['PubmedArticle']):
                    title = paper['MedlineCitation']['Article']['ArticleTitle']
                    authors = ', '.join([author['LastName'] for author in paper['MedlineCitation']['Article']['AuthorList']])
                    year_list = paper['MedlineCitation']['Article']['ArticleDate']
                    year = year_list[0].get('Year', '') if year_list else ''
                    link = f"https://www.ncbi.nlm.nih.gov/pubmed/{paper['MedlineCitation']['PMID']}"

                    all_papers.append({
                        "Query": query,
                        "Title": title,
                        "Authors": authors,
                        "Year": year,
                        "Link": link
                    })
                    time.sleep(2)  # Sleep for 2 seconds between requests

                df = pd.DataFrame(all_papers)
                filename = f'{output_directory}/PubMED/PubMed_results.csv'
                df.to_csv(filename, index=False)  # Save DataFrame to CSV file
        return all_papers
    
    return process_searches(search_strings, PubMed_num_of_articles, output_directory)