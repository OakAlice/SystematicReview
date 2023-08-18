# SystematicReview

This is a workflow for quickly gathering unique papers from multiple search strings from multiple databases. It works by sending search queries to various databases and scraping the citation information for the first 'n' papers from each, then collating these and removing duplicates to present a csv of unique paper titles with authors, publishing year, links, and abstracts. This is my first ever python project so is absolutely terrible.

Input Variables and Run the Code
* [UserInput.py](https://github.com/OakAlice/SystematicReview/blob/main/UserInput.py) creates the unique search strings from sets of keyword synonyms, user inputs all variables, then calls and runs all other code sections (individually below)

Search the Databases
* [ScholarStringToUrl.py](https://github.com/OakAlice/SystematicReview/blob/main/ScholarStringToUrl.py)  [SearchScholar.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScholar.py) and [TidyScholar.py](https://github.com/OakAlice/SystematicReview/blob/main/TidyScholar.py) are for scraping and formatting for Google Scholar. This has a very high probability of being blocked and I was unable to use it.
* [SearchScopus.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScopus.py)
* [SearchPubMed.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchPubMed.py)
* [SearchCORE.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchCORE.py)
* [SearchArXiv.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchArXiv.py) # only include if you're searching for pre-prints too
* [SearchScienceDirect.py](https://github.com/OakAlice/SystematicReview/blob/main/SearchScienceDirect.py)
* [SearchSemantic.py]
* [SearchWoS.py]

Combining and Completing
* [Combining.py](https://github.com/OakAlice/SystematicReview/blob/main/Combining.py) stitches together tidied csvs and removes cross-database duplication
* [GettingAbstracts.py](https://github.com/OakAlice/SystematicReview/blob/main/GettingAbstracts.py) retrives the full abstract for papers that weren't retrived from the above databases (doesn't work for every paper btw)

And then you're done. Should have a lot of hefty papers worth searching through.
