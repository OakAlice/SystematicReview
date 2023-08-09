# Searching IEEE for more papers
# require a functioning API key (can only request during work hours it seems????)

import requests
import csv

def QueryIEEE(search_strings, num_of_articles, output_directory, IEEEKey):
    
    BASE_URL = "http://ieeexploreapi.ieee.org/api/v1/search/articles"

    all_papers = []
    for query in search_strings:
        # Construct the parameters for API request
        params = {
            'apikey': IEEEKey,
            'format': 'json',
            'querytext': query,
            'max_records': num_of_articles,  # Limit number of articles
        }

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if 'articles' in data:
            for article in data['articles']:
                title = article.get('title', 'N/A')
                authors = ', '.join([author.get('full_name', 'N/A') for author in article.get('authors', [])])
                year = article.get('publication_year', 'N/A')
                link = article.get('pdf_url', 'N/A')
                abstract = article.get('abstract', 'N/A')

                all_papers.append({
                    "Query": query,
                    "Title": title,
                    "Authors": authors,
                    "Year": year,
                    "Link": link,
                    "Abstract": abstract
                })
                
    # Write data to a CSV file
    csv_file_path = f"{output_directory}/IEEE_Results.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Query", "Title", "Authors", "Year", "Link", "Abstract"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for paper in all_papers:
            writer.writerow(paper)

    print(f"IEEE data saved to {csv_file_path}")


# test run
search_queries = ["animal", "behaviour"]
num_articles = 10
output_dir = "C:/Users/oakle/OneDrive/Documents/Systematic Results"
api_key = "YOUR_IEEE_XPLORE_API_KEY"

# Call the function
QueryIEEE(search_queries, num_articles, output_dir, api_key)