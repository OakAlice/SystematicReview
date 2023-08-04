# SystematicReview

I am doing a systematic literature review and want to gather as many papers on this topic as I can. This is a workflow for gathering papers. 

* SearchStrings.py creates the unique search strings from sets of keyword synonyms
Google Scholar
* ScholarStringToUrl.py converts these strings to approporiate url for Google Scholar
* SearchScholar.py requests Google Scholar information from each urls and pulls the key citation information
* ScholarResultsTidying.py collates and tidys the csv results and removes duplicates
Scopus
* SearchScopus.py used Scopus Search API to access Scopus paper infomation
* ScopusResultsTidying.py collates the scopus results and removes duplicates