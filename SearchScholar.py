## Searching google scholar with the search strings
# instructions from @nandinisaini021 on medium

# packages
import requests 
import pandas as pd
from bs4 import BeautifulSoup
import re
from time import sleep
import os

# where you want the search results to save to
output_directory = "C:/Users/oakle/OneDrive/Documents/Systematic Results"
os.makedirs(output_directory, exist_ok=True)

# my stuff
from ScholarStringsToUrl import all_urls

# required to allow us to access the page
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

# function for getting info of the web page
def get_paperinfo(paper_url):
    # download the page
    response = requests.get(paper_url, headers=headers)

    # check successful response
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')

    # parse using beautiful soup
    paper_doc = BeautifulSoup(response.text, 'html.parser')

    return paper_doc

def get_citation_count(paper_url):
    response = requests.get(paper_url, headers=headers)
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page')

    paper_doc = BeautifulSoup(response.text, 'html.parser')
    
    citation_tag = paper_doc.select_one('.gs_citi')
    if citation_tag:
        citation_text = citation_tag.text
        citation_count = int(re.search(r'\d+', citation_text).group()) if re.search(r'\d+', citation_text) else 0
        return citation_count
    else:
        return 0

# extracting the papers' tags
def get_tags(doc):
    paper_tag = doc.select('.gs_r.gs_or.gs_scl')
    link_tag = doc.select('.gs_rt a')
    author_tag = doc.select('.gs_a')

    return paper_tag, link_tag, author_tag

# paper title
def get_papertitle(paper_tag):
    paper_names = []
    for tag in paper_tag:
        paper_names.append(tag.select_one('.gs_rt a').text.strip())
    return paper_names

# function for url
def get_link(link_tag):
    links = []
    for tag in link_tag:
        links.append(tag['href'])
    return links

# function for author, year, and publication info
def get_author_year_publi_info(author_tag):
    years = []
    publications = []
    authors = []
    for tag in author_tag:
        authortag_text = tag.text.strip()
        year = int(re.search(r'\d+', authortag_text).group()) if re.search(r'\d+', authortag_text) else 'N/A'
        years.append(year)
        publication = authortag_text.split(' - ')[-1].strip() if ' - ' in authortag_text else 'N/A'
        publications.append(publication)
        author = ' '.join(authortag_text.split(' - ')[0].split(',')[:2]).strip()
        authors.append(author)
    return years, publications, authors

# adding information in repository
def add_in_paper_repo(papername, year, author, publi, link, url_column):
    paper_repos_dict['Title'].extend(papername)
    paper_repos_dict['Year'].extend(year)
    paper_repos_dict['Author'].extend(author)
    paper_repos_dict['Publication'].extend(publi)
    paper_repos_dict['Url'].extend(link)
    paper_repos_dict['Source'].extend(url_column)
    return pd.DataFrame(paper_repos_dict)

i = 0
for url in all_urls:
    # creating final repository
    paper_repos_dict = {
        'Title': [],
        'Year': [],
        'Author': [],
        'Publication': [],
        'Url': [],
        'Source': [],
        'Citations': []
    }

    # Loop through the Google Scholar search results in sets of 10 (e.g., 0 to 9, 10 to 19, etc.).
    for j in range(0, 1000, 10): # get the first 1000 papers
        # get url for each page
        this_url = url.format(i)

        # function for the get content of each page
        doc = get_paperinfo(this_url)

        # function for the collecting tags
        paper_tag, link_tag, author_tag = get_tags(doc)

        # paper title from each page
        papername = get_papertitle(paper_tag)

        # year, author, publication of the paper
        year, publication, author = get_author_year_publi_info(author_tag)

        # url of the paper
        link = get_link(link_tag)

        # add the source URL
        url_column = [this_url] * len(papername)

        # get the number of citations
        citation_counts = [get_citation_count(link) for link in link]

        # add in paper repo dict
        final = add_in_paper_repo(papername, year, author, publication, link, url_column)
        
        # add the citation counts to the DataFrame
        final['Citations'] = citation_counts

        # use sleep to avoid status code 429
        sleep(3)

    csv_file_name = os.path.join(output_directory, f'results_{i + 1}.csv')
    print(csv_file_name)
    final.to_csv(csv_file_name, index=False)
    i += 1