# SystematicReview

I am doing a systematic literature review and want to gather as many papers on this topic as I can. This is a workflow for quickly gathering unique papers from multiple search strings from multiple databases. It works by sending search queries to Scholar, Scopus and PubMED and scraping the citation information for the first >1000 papers from each, then collating these and removing duplicates to present a csv of unique paper titles with authors, publishing year, and links to each.

* SearchStrings.py creates the unique search strings from sets of keyword synonyms
Google Scholar
* ScholarStringToUrl.py converts these strings to approporiate url for Google Scholar
* SearchScholar.py requests Google Scholar information from each urls and pulls the key citation information
* ScholarResultsTidying.py collates and tidys the csv results and removes duplicates
Scopus
* SearchScopus.py used Scopus Search API to access Scopus paper infomation
* ScopusResultsTidying.py collates the scopus results and removes duplicates
PubMED
* SearchPubMed.py used Biopython and PubMED API to access PubMED paper information
* PubMedResultsTidying.py removes duplicates

* Integration.py stitches together the tidied csvs from each and removes cross-database duplication