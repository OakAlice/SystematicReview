# When we have achieved the finalised list of unique papers, get the abstracts
from Bio import Entrez
from scholarly import scholarly
import pandas as pd
import re
from pyscopus import Scopus
import urllib.parse
import requests

def fetch_PubMed_abstracts(pmids, PubMedEmail):
    # ID required to access the papers
    Entrez.email = PubMedEmail
    handle = Entrez.efetch(db="pubmed", id=pmids, rettype="abstract", retmode="text")
    return handle.read()

def fetch_Scholar_abstracts(title):
    search_query = scholarly.search_pubs(title)
    try:
        paper = next(search_query)
    except StopIteration:
        return None
    if paper and 'abstract' in paper:
        return paper['abstract']
    return None

def fetch_Scopus_abstracts(scopus_id, ScopusKey):
    headers = {
        'Accept': 'application/json',
        'X-ELS-APIKey': ScopusKey,
    }
    url = f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'abstracts-retrieval-response' in data:
        if 'coredata' in data['abstracts-retrieval-response']:
            if 'dc:description' in data['abstracts-retrieval-response']['coredata']:
                return data['abstracts-retrieval-response']['coredata']['dc:description']
    return None

def fetch_abstracts(output_directory, PubMedEmail, ScopusKey):
    df = pd.read_csv(f'{output_directory}/Unique_papers.csv')
    df['Abstract'] = ''
    for idx, row in df.iterrows():
        if row['Database'] == 'PubMed':
            link = row['Link']
            pmid = re.findall(r'\d+', link)[-1]
            df.at[idx, 'Abstract'] = fetch_PubMed_abstracts([pmid], PubMedEmail)
        elif row['Database'] == 'Scholar':
            df.at[idx, 'Abstract'] = fetch_Scholar_abstracts(row['Title'])
        elif row['Database'] == 'Scopus':
            link = row['Link']
            parsed = urllib.parse.urlparse(link)
            scopus_id = parsed.path.split('/')[-1]
            df.at[idx, 'Abstract'] = fetch_Scopus_abstracts(scopus_id, ScopusKey)
    
    # print to csv
    csv_file_name = f'{output_directory}/Abstract_papers.csv'
    df.to_csv(csv_file_name, index=False)


from UserInput import output_directory
from UserInput import PubMedEmail
from UserInput import ScopusKey
fetch_abstracts(output_directory, PubMedEmail, ScopusKey)


