# SystematicReview

I am doing a systematic literature review and want to gather as many papers on this topic as I can. This is a workflow for gathering papers. 

* SearchStrings.py creates the unique search strings from sets of keyword synonyms. 
* StringToUrl.py converts these strings to approporiate url addresses for each of the databases. 
* Search.py requests page information from each of the urls and pulls the key citation information. 
* ResultsTidying.py tidys the csv results for ready comparison and analysis. 