# search arXiv for the papers

import requests
import feedparser
import pandas as pd

def QueryArxiv(search_strings, Num_of_articles, output_directory):
    base_url = "http://export.arxiv.org/api/query?"
    search_queries = [' AND '.join(words) for words in search_strings]
    papers = []

    for query in search_queries:
        # Forming the query string
        params = {
            "search_query": f"all:{query}",
            "start": 0,   # start from the beginning
            "max_results": Num_of_articles  # limit to 10 results for this example
        }

        response = requests.get(base_url, params=params)

        # Parsing the response using feedparser
        feed = feedparser.parse(response.content)

        for entry in feed.entries:
            title = entry.title
            authors = ', '.join([author.name for author in entry.authors])
            link = entry.link
            year = entry.published_parsed.tm_year  # Get the publishing year
            abstract = entry.summary

            papers.append({
                "Query": query,
                "Title": title,
                "Authors": authors,
                "Year": year,
                "Citations": None,
                "Link": link,
                "Abstract": abstract
            })

    # Convert to DataFrame
    df = pd.DataFrame(papers)

    # Save to CSV
    filepath = f"{output_directory}/arxiv_results.csv"
    df.to_csv(filepath, index=False)
    print(f"Arxiv results saved to {filepath}")
