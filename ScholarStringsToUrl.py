## Convert the strings to URLs for Google Scholar

from SearchStrings import search_strings

scholar_base = "https://scholar.google.com/scholar?q=words+here+&hl=en&as_sdt=0%2C5&as_ylo=2013&as_yhi=2023"

# empty space for the urls
all_urls = []

# Iterate over each set of search strings
for search_set in search_strings:
    # Join the search strings in the set with '+' and replace spaces with %20 for scholar_base
    replacement_scholar = "+AND+".join(search_set)
    replacement_scholar = replacement_scholar.replace(' ', '%20')
    # Replace "words+here" in the base URL with the replacement for scholar_base
    url_scholar = scholar_base.replace("words+here", replacement_scholar)

    # Append both scholar_base and scopus_base URLs into the list
    all_urls.append(url_scholar)

print(all_urls)