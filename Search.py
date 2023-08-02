## Searching the databases with the search strings
# instructions from @nandinisaini021 on medium

# packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from time import sleep

# my stuff
from StringsToUrl import all_urls

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
    paper_repos_dict['Paper Title'].extend(papername)
    paper_repos_dict['Year'].extend(year)
    paper_repos_dict['Author'].extend(author)
    paper_repos_dict['Publication'].extend(publi)
    paper_repos_dict['Url of paper'].extend(link)
    paper_repos_dict['Source url'].extend(url_column)
    return pd.DataFrame(paper_repos_dict)

i = 0
for url in all_urls:
    # creating final repository
    paper_repos_dict = {
        'Paper Title': [],
        'Year': [],
        'Author': [],
        'Publication': [],
        'Url of paper': [],
        'Source url': [] 
    }

    # Loop through the Google Scholar search results in sets of 10 (e.g., 0 to 9, 10 to 19, etc.).
    for j in range(0, 30, 10):
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

        # add in paper repo dict
        final = add_in_paper_repo(papername, year, author, publication, link, url_column)

        # use sleep to avoid status code 429
        sleep(30)

    csv_file_name = f'google_scholar_results_{i + 1}.csv'
    print(csv_file_name)
    final.to_csv(csv_file_name, index=False)
    i+=1