## Searching PubMed for even more citations yay
# tutorial from https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/


# pip install biopython
import pandas as pd
from SearchStrings import search_strings
import time
from Bio import Entrez
from requests.exceptions import HTTPError

# where you want to save the files
output_directory = "C:/Users/oakle/OneDrive/Documents/Systematic Results/PubMED"

# Set email (required by NCBI API)
Entrez.email = 'oaw001@student.usc.edu.au'

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
    except HTTPError as e:
        print("An error occurred while fetching details:", e)
        return None

if __name__ == '__main__':
    search_queries = [' AND '.join(words) for words in search_strings]
    num_of_articles = 1000

    all_papers = []
    i = 0
    for query in search_queries:
        results = search(query)
        print(query) # test print
        
        if results and 'IdList' in results and len(results['IdList']) > 0:
            id_list = results['IdList'][:num_of_articles]
            papers = fetch_details(id_list)

            if papers:
                for i, paper in enumerate(papers['PubmedArticle']):
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

                if all_papers:
                    df = pd.DataFrame(all_papers)
                    filename = f'{output_directory}/PubMed_results_{i}.csv'
                    df.to_csv(filename, index=False)  # Save DataFrame to CSV file
                    print(f"Results for '{query}' saved to '{filename}'")
                else:
                    print(f"No valid records found for '{query}'")
            else:
                print(f"No records found for '{query}'")
            i +=1