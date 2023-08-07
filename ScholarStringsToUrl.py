## define a function to convert the strings to URLs for Google Scholar

def generate_scholar_urls(search_strings):
    urls = []

    for search_set in search_strings:
        # Join the search strings in the set with '+' and replace spaces with %20 for scholar_base
        replacement_scholar = "+AND+".join(search_set).replace(' ', '%20')
        urls.append(f"https://scholar.google.com/scholar?q={replacement_scholar}+&hl=en&as_sdt=0%2C5&as_ylo=2013&as_yhi=2023")
    
    return urls