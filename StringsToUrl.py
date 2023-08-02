## Convert the strings to URLs

from SearchStrings import search_strings

base_url = "https://scholar.google.com/scholar?q=words+here+&hl=en&as_sdt=0%2C5&as_ylo=2013&as_yhi=2023"

# empty space for the urls
all_urls = [] 

# Iterate over each set of search strings
for search_set in search_strings:
    # Join the search strings in the set with '+' and replace spaces with %20
    replacement = "+".join(search_set)
    replacement = replacement.replace(' ', '%20')

    # Replace "words+here" in the base URL with the replacement
    url = base_url.replace("words+here", replacement)

    # sppend into a list
    all_urls.append(url)