# Searching CORE in the same method


#### SEMI FUNCTIONAL, RETURNS RESULTS, BUT THEY AREN'T LINKED TO THE SEARCH TERMS
# Suspect that the search terms are being sent as letters rather than words or somethign?

from typing import Any, Dict, List
import pandas as pd
from core_api import CoreClient, CoreFindResult


def search_core(c: CoreClient, q: str, Num_of_articles) -> List[CoreFindResult]:
    resp: List[Dict[str, Any]] = c.find(query=q, year_min=2013, limit=Num_of_articles)
    return [
        CoreFindResult(**x) for x in resp
    ]

def QueryCore(output_directory, search_strings, COREKey, Num_of_articles):
    papers = []
    search_queries = [' AND '.join(words) for words in search_strings]
    c = CoreClient(api_key=COREKey)
    for query in search_queries:
        results = search_core(c, query, Num_of_articles)
        for r in results:
            links = list(filter(lambda x: x.get("type", "") == "reader", r.links))
            papers.append({
                "Query": query,
                "Title": r.title,
                "Authors":  [n['name'] for n in r.authors],
                "Year": r.yearPublished,
                "Citations": None,
                "Link": links[0]["url"] if len(links) > 0 else None,
                "Abstract": r.abstract
            })

    # Convert to DataFrame
    df = pd.DataFrame(papers)

    # Save to CSV
    filepath = f"{output_directory}/core_results.csv"
    df.to_csv(filepath, index=False)
    print(f"Results saved to {filepath}")
