import requests
import csv
from time import sleep

def QuerySemantic(search_strings, output_directory, SemanticKey, offset=0, limit=10):
    # Function to query Semantic Scholar and save results to CSV
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {"x-api-key": SemanticKey}

    # Joining the search strings with 'AND' for the query
    query_string = ' AND '.join(search_strings)

    params = {
        "query": query_string,
        "offset": offset,
        "limit": limit,
        "fields": "title"
    }

    # Query Semantic Scholar
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return

    results = response.json()

    # Save to CSV
    csv_file_path = f"{output_directory}/semantic_scholar_results.csv"
    with open(csv_file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # If file is empty, write the header
        if file.tell() == 0:
            writer.writerow(["Title"])

        for paper in results.get('data', []):
            title = paper.get('title', '')
            writer.writerow([title])

    print(f"Added {len(results.get('data', []))} papers to the CSV")
    sleep(1)
