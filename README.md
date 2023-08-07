# SystematicReview

I am doing a systematic literature review and want to gather as many papers on this topic as I can. This is a workflow for quickly gathering unique papers from multiple search strings from multiple databases. It works by sending search queries to Scholar, Scopus and PubMED and scraping the citation information for the first >1000 papers from each, then collating these and removing duplicates to present a csv of unique paper titles with authors, publishing year, and links to each.

Input Variables and Run the Code
* [UserInput.py](https://github.com/OakAlice/SystematicReview/blob/main/UserInput.py) creates the unique search strings from sets of keyword synonyms, user inputs all variables, then calls and runs all other code sections (individually below)

Google Scholar
* [ScholarStringToUrl.py](https://github.com/OakAlice/SystematicReview/blob/main/ScholarStringToUrl.py) converts keyword strings to approporiate url for Google Scholar
* [SearchScholar.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScholar.py) requests Google Scholar page from each url and pulls key citation information
* [TidyScholar.py](https://github.com/OakAlice/SystematicReview/blob/main/TidyScholar.py) collates, tidys, removes duplicates

Scopus
* [SearchScopus.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScopus.py) used Scopus Search API to access Scopus paper infomation
* [TidyScopus.py](https://github.com/OakAlice/SystematicReview/blob/main/TidyScopus.py) collates, renames columns, removes duplicates

PubMED
* [SearchPubMed.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchPubMed.py) used Biopython and PubMED API to access PubMED paper information
* [TidyPubMed.py](https://github.com/OakAlice/SystematicReview/blob/main/TidyPubMed.py) removes duplicates, tidies

Combining
* [Combining.py](https://github.com/OakAlice/SystematicReview/blob/main/Combining.py) stitches together tidied csvs and removes cross-database duplication
