# User input and code initialisation page
# it works in theory, but many of the individual search systems don't work anymore..

from itertools import product

# enter the keywords to search for where each row is a concept with synonyms
A1 = ['accelerometer', 'IMU', 'accelerometry']
A2 = ['activity recognition', 'behaviour',] 
A3 = ['machine learning', 'classification'] 
B = ['wildlife', 'animal']
C = ['supervised', 'unsupervised']

# define the concept combinations you'd want to search for
combinations_a = list(product(A1, A2, A3, B, C))

# add together to form one list, if necessary
search_strings = combinations_a

# the parent directory where the results should be saved
output_directory = "C:/Users/oakle/Documents/PhD docs/Systematic Results/DecemberRedo/Third_attempt"

# number of articles per search from each of the strings
Num_of_articles = 100

# API keys
ScopusKey = 'fdbb42b4b0363feb81cf4551863b0279' # Elsevier's Scopus Search API
PubMedEmail = 'oaw001@student.usc.edu.au' # PubMed email account
COREKey = "XXXX" # for CORE Api
SemanticKey = 'XBlMKbMLsO1pCQSj9zbQDaW7MrGOSvlS9OGo6cko' # for Semantic Scholar
scienceDIrectKey = '9b54f4ad7b44a3e31256ec633cc7014c' # not working for some reason
# The script is now ready to run

# import the functions from each of the individual scripts

#from ScholarStringsToUrl import generate_scholar_urls
#from SearchScholar2 import QueryScholar
#from TidyScholar import TidyingScholarResults

#from SearchArXiv import QueryArxiv
#from SearchCORE import QueryCore

from SearchScopus import QueryScopus
from SearchPubMed import QueryPubMed
from SearchScienceDirect import QueryScienceDirect
from SearchSematic import QuerySemantic

from Combining import CombiningDatabases
#from GettingAbstracts import get_abstracts

# call and run all the scripts with these variables
def main():
    #urls = generate_scholar_urls(search_strings)
    #QueryScholar(urls, Num_of_articles, output_directory)
    #TidyingScholarResults(output_directory)
    #QueryArxiv(search_strings, Num_of_articles, output_directory)
    #QueryCore(output_directory, search_strings, COREKey, Num_of_articles)
    
    #QueryScopus(ScopusKey, search_strings, output_directory, Num_of_articles)
    #QueryPubMed(search_strings, Num_of_articles, output_directory, PubMedEmail)
    #QuerySemantic(search_strings, output_directory, SemanticKey)
    #QueryScienceDirect(search_strings, Num_of_articles, scienceDIrectKey, output_directory)
        
    CombiningDatabases(output_directory)
    #get_abstracts(output_directory, PubMedEmail)

if __name__ == "__main__":
    main()

# you should now have a csv file with lots of relevant papers and their info
