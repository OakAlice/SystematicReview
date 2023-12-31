## Searching google scholar with the search strings
# instructions from @nandinisaini021 on medium

# packages
import requests 
import pandas as pd
from bs4 import BeautifulSoup
import re
from time import sleep
import os

#from ScholarStringsToUrl import generate_scholar_urls
#from UserInput import search_strings
#urls = generate_scholar_urls(search_strings)

def QueryScholar(urls, Num_of_articles, output_directory):

    # required to allow us to access the page
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    scholar_directory = os.path.join(output_directory, 'Scholar')
    os.makedirs(scholar_directory, exist_ok=True)

    # CSV file path
    csv_file_name = os.path.join(scholar_directory, 'results.csv')

    # Check if file exists, if not create it with headers
    if not os.path.isfile(csv_file_name):
        pd.DataFrame(columns=['Title', 'Year', 'Authors', 'Publication', 'Link', 'Source', 'Citations']).to_csv(csv_file_name, index=False)

    # function for getting info of the web page
    def get_paperinfo(paper_url):
        # download the page
        response = requests.get(paper_url, headers=headers)
        print(response)

        # parse using beautiful soup
        paper_doc = BeautifulSoup(response.text, 'html.parser')

        return paper_doc

    # extracting the papers' tags
    def get_tags(doc):
        paper_tag = [doc ]# .select('.gs_r.gs_or.gs_scl')[0]
        link_tag = doc.select('.gs_rt a[data-clk-atid]')
        author_tag = doc.select('.gs_a')
        citation_tags = doc.select('.gs_flb a[href^="/scholar?cites"]')

        return {
            "paper": paper_tag[0],
            "link": link_tag[0],
            "author": author_tag[0],
            "citations": citation_tags[0] if len(citation_tags) > 0 else 0
        }

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

    all_data = []
    print(f"number of urls: {len(urls)}")

    for url in urls:
        for j in range(0, Num_of_articles, 10):  # get the first papers
            this_url = url.format(j)
             
            doc = get_paperinfo(this_url)
            # Check if doc contains any data
            if not doc:
                print("Failed to fetch or parse data from:", this_url)
                continue

            papers = [get_tags(d) for d in doc.select("div[data-rp]")]
            print(url)
            print(f"Number of papers: {len(papers)}")
            paper_tag = [p["paper"] for p in papers]
            link_tag =  [p["link"] for p in papers]
            author_tag = [p["author"] for p in papers]
            citation_counts = [p["citations"] for p in papers]

            papername = get_papertitle(paper_tag)
            year, publication, author = get_author_year_publi_info(author_tag)
            link = get_link(link_tag)
            url_column = [this_url] * len(papername)

            # Store each paper's data
            for i in range(len(papername)):
                all_data.append({
                    'Title': papername[i],
                    'Year': year[i],
                    'Authors': author[i],
                    'Publication': publication[i],
                    'Link': link_tag[i]['href'],
                    'Source': url_column[i],
                    'Citations': citation_counts[i]
                })

            # Append this batch of data to the CSV file
            df = pd.DataFrame(all_data)
            df.to_csv(csv_file_name, mode='a', header=False, index=False)

            sleep(3)

    # Convert all collected data to a DataFrame
    df = pd.DataFrame(all_data)
    csv_file_name = os.path.join(output_directory, 'Scholar/results.csv')
    df.to_csv(csv_file_name, index=False)
