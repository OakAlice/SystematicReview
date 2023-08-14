# SystematicReview

This is a workflow for quickly gathering unique papers from multiple search strings from multiple databases. It works by sending search queries to various databases and scraping the citation information for the first 'n' papers from each, then collating these and removing duplicates to present a csv of unique paper titles with authors, publishing year, links, and abstracts. An influence metric is generated from the citations and journal, from which the top papers are selected.

Input Variables and Run the Code
* [UserInput.py](https://github.com/OakAlice/SystematicReview/blob/main/UserInput.py) creates the unique search strings from sets of keyword synonyms, user inputs all variables, then calls and runs all other code sections (individually below)

Search the Databases
* [ScholarStringToUrl.py](https://github.com/OakAlice/SystematicReview/blob/main/ScholarStringToUrl.py) converts keyword strings to approporiate url for Google Scholar
* [SearchScholar.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScholar.py)
* [SearchScopus.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScopus.py)
* [SearchPubMed.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchPubMed.py)
* [SearchCORE.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchCORE.py)
* [SearchArXiv.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchArXiv.py)
* [SearchScienceDirect.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScienceDirect.py)

Combining and Completing
* [Combining.py](https://github.com/OakAlice/SystematicReview/blob/main/Combining.py) stitches together tidied csvs and removes cross-database duplication
* [GettingAbstracts.py](https://github.com/OakAlice/SystematicReview/blob/main/GettingAbstracts.py) retrives the full abstract for papers that weren't retrived from the above databases (doesn't work for every paper btw)
* [GettingImpact.py](https://github.com/OakAlice/SystematicReview/blob/main/GettingImpact.py) gets the citation count and journal for each paper, generates a metric for the paper's influence/importance

Final Summarisation
Manually go through the resultant dataframe to remove all irrelevant papers. When the list has been slimmed as much as possible, proceed. 
* [AbstractsToChat.py](https://github.com/OakAlice/SystematicReview/blob/main/AbstractsToChat.py) queries Chat with the title and abstract, requesting key summary and information which is stored in a csv.
