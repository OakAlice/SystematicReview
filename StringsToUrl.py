## Convert the strings to URLs

from SearchStrings import search_strings

scholar_base = "https://scholar.google.com/scholar?q=words+here+&hl=en&as_sdt=0%2C5&as_ylo=2013&as_yhi=2023"
scopus_base = "https://www.scopus.com/results/results.uri?sort=plf-f&src=s&st1=accelerometer&sid=747e878fe2abe65eec60cd5aee3cc070&sot=b&sdt=b&sl=56&s=TITLE-ABS-KEY%28words%2C+here%29&origin=searchbasic&editSaveSearch=&yearFrom=2013&yearTo=Present&sessionSearchId=747e878fe2abe65eec60cd5aee3cc070&limit=10"

# empty space for the urls
all_urls = []

# Iterate over each set of search strings
for search_set in search_strings:
    # Join the search strings in the set with '+' and replace spaces with %20 for scholar_base
    replacement_scholar = "+AND+".join(search_set)
    replacement_scholar = replacement_scholar.replace(' ', '%20')
    # Replace "words+here" in the base URL with the replacement for scholar_base
    url_scholar = scholar_base.replace("words+here", replacement_scholar)

    # Join the words in the set with '%2C+' for scopus_base
    replacement_scopus  = "%2C+".join(search_set)
    replacement_scopus = replacement_scopus.replace(' ', '%2C+')
    # Replace "words%2C+here" in base URL with the replacement for scopus_base
    url_scopus = scopus_base.replace("words%2C+here", replacement_scopus)

    # Append both scholar_base and scopus_base URLs into the list
    all_urls.append(url_scholar)
    #all_urls.append(url_scopus)

print(all_urls)