# due to Google Scholar scraping restrictions, will instead take the abstract from each website

import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from Bio import Entrez
import re
from time import sleep

def get_abstracts(output_directory, PubMedEmail):

    # get the journal name from the link
    def extract_journal_name(url):
        netloc = urllib.parse.urlparse(url).netloc
        # Split the netloc by '.' and retrieve the part just after the 'www' or after the '//'
        parts = netloc.split('.')
        if parts[0] == 'www':
            return parts[1]
        else:
            return parts[0]
        
    # function to get the html of any site returning as a soup
    def get_html(url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(response.text, 'html.parser')        
            return soup
        except requests.HTTPError as e:
            if e.response.status_code == 403:  # If Forbidden error, print a message and return None
                print(f"Skipping URL due to 403 Forbidden error: {url}")
                return None
            print(f"Error fetching URL {url}: {e}")
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
        return None

    # series of functions that extract the abstract from each of the journal types

    # PubMed - using the API
    def fetch_PubMed_abstracts(pmids, PubMedEmail):
        # ID required to access the papers
        Entrez.email = PubMedEmail
        handle = Entrez.efetch(db="pubmed", id=pmids, rettype="abstract", retmode="text")
        return handle.read()

    # now using generic webscraping
    # handing getting the text out of the html
    def extract_text(element):
        if not element:
            return None
        # Convert the Beautiful Soup element to a string and strip it
        text = str(element)
        # Remove any HTML/XML tags from the text
        clean_text = re.sub('<.*?>', '', text)
        
        return clean_text.strip()

    # now the specific calls for each site
    def scrape_mdpi(soup):
        return extract_text(soup.find('section', class_='html-abstract'))

    def scrape_ieeex(soup):
        abstract_section = soup.select_one('meta[property="og:description"]')
        return abstract_section['content'].strip() if abstract_section else None

    def scrape_plos(soup):
        return extract_text(soup.find('div', class_='abstract-content'))

    def scrape_sciencedirect(soup):
        return extract_text(soup.find('p', id='abspara0010'))

    def scrape_springer(soup):
        return extract_text(soup.find('class', id='Abs1-content'))

    def scrape_acmdl(soup):
        abstract_div = soup.find('div', class_='abstractSection abstractInFull')
        return extract_text(abstract_div)

    def scrape_nature(soup):
        return extract_text(soup.find('div', id='Abs1-content'))

    def scrape_besjournals(soup):
        abstract_div = extract_text(soup.find('div', class_='article-section__content en main'))
        return abstract_div.get_text(strip=True) if abstract_div else None


    # main function
    def process_abstracts(output_directory, PubMedEmail):
        # Load the dataframe
        df = pd.read_csv(f'{output_directory}/Unique_papers.csv')
        df['Journal'] = ''
        df['Abstract'] = ''

        # Mapping the journal names to their respective functions
        journal_function_map = {
            'mdpi': scrape_mdpi,
            'dl': scrape_acmdl,
            'besjounrnals': scrape_besjournals,
            'ieeexplore': scrape_ieeex,
            'nature': scrape_nature,
            'journals': scrape_plos,  # journals is the name for plos
            'sciencedirect': scrape_sciencedirect,
            'link': scrape_springer   # springer
        }

        for idx, row in df.iterrows():
            # Skip if the link is empty or NaN
            if pd.isnull(row['Link']) or row['Link'] == '':
                continue
            
            link = row['Link']
            extracted_journal = extract_journal_name(link)

            try:             
                if row['Database'] == 'PubMed':
                    pmid = re.findall(r'\d+', link)[-1]
                    abstract = fetch_PubMed_abstracts([pmid], PubMedEmail)
                elif extracted_journal in journal_function_map:
                    soup = get_html(link)
                    print(f"Processing link: {link}")
                    
                    if soup is None: # because some sites block me so I get "Forbidden"
                        continue
                    if not soup:
                        print(f"Error getting soup for link: {link}")
                        continue

                    abstract = journal_function_map[extracted_journal](soup)
                else:
                    continue
        
                df.at[idx, 'Abstract'] = abstract

            except Exception as e:
                print(f"Error fetching abstract for {row['Title']} from {row['Database']} with link {row['Link']}. Error: {e}")
                continue
            sleep(1)
                    
        csv_file_name = f'{output_directory}/Abstract_papers.csv'
        df.to_csv(csv_file_name, index=False)

    process_abstracts(output_directory, PubMedEmail)
